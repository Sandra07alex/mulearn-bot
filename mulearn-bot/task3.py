#task 3
import discord
from discord.ext import commands
import mysql.connector

from apikeys import BOT_TOKEN, DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE

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

# Create a table named 'user_role' if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_role (
        discord_id VARCHAR(255),
        role VARCHAR(255)
    )
""")


# Slash command to select a role
@client.command()
async def select_role(ctx):
    try:
        # Define available roles (change as needed)
        roles = ['Role1', 'Role2', 'Role3']

        # Create select menu options
        options = [
            discord.SelectOption(label=role, value=role)
            for role in roles
        ]

        # Create and send the select menu
        select = discord.ui.Select(
            placeholder='Select a role',
            options=options
        )
        msg = await ctx.send('Please select your role:', view=select)

        # Wait for user selection
        interaction = await client.wait_for(
            'select_option',
            check=lambda i: i.component and i.component.custom_id == select.custom_id,
            timeout=60
        )

        # Update role in database
        selected_role = interaction.values[0]
        cursor.execute("""
            REPLACE INTO user_role (discord_id, role) VALUES (%s, %s)
        """, (str(ctx.author.id), selected_role))
        db.commit()

        # Grant the selected role to the user
        role = discord.utils.get(ctx.guild.roles, name=selected_role)
        await ctx.author.add_roles(role)

        await ctx.send(f"Role {selected_role} selected successfully!")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


client.run(BOT_TOKEN)
