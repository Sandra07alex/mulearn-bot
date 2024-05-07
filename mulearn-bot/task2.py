import discord
from discord.ext import commands
import mysql.connector

from apikeys import BOT_TOKEN, DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE2

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = commands.Bot(command_prefix='/', intents=intents)

# Connect to the MySQL database
db = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_DATABASE
)
cursor = db.cursor()

# Create a table named 'user_words' if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_words (
        discord_id VARCHAR(255),
        word VARCHAR(255)
    )
""")

@client.event
async def on_ready():
    print("The bot is now ready to use")

@client.event
async def on_message(message):
    if message.author.bot:
        return
    # Extract words from the message
    words = message.content.split()

    # Store each word in the database along with the user's ID
    for word in words:
        cursor.execute("""
            INSERT INTO user_words (discord_id, word) VALUES (%s, %s)
        """, (str(message.author.id), word))
        db.commit()

@client.command()
async def word_status(ctx):
    try:
        # Execute MySQL query to get the 10 most used words
        cursor.execute("""
            SELECT word, COUNT(*) AS count FROM user_words GROUP BY word ORDER BY count DESC LIMIT 10
        """)
        results = cursor.fetchall()

        if results:
            word_status_str = "\n".join([f"{row[0]}: {row[1]} times" for row in results])
            await ctx.send(f"Most used words:\n{word_status_str}")
        else:
            await ctx.send("No words found in the database.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@client.command()
async def user_status(ctx, user: discord.User):
    # Get the 10 most used words by the specified user from the database
    cursor.execute("""
        SELECT word, COUNT(*) AS count FROM user_words WHERE discord_id = %s GROUP BY word ORDER BY count DESC LIMIT 10
    """, (str(user.id),))
    results = cursor.fetchall()

    if results:
        user_status_str = "\n".join([f"{row[0]}: {row[1]} times" for row in results])
        await ctx.send(f"Most used words by {user.name}:\n{user_status_str}")
    else:
        await ctx.send(f"No words found for {user.name} in the database.")

client.run(BOT_TOKEN)
