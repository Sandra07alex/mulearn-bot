
## Task 1
##Welcome Card Implementation
import discord
from discord.ext import commands

from apikeys import BOT_TOKEN

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = commands.Bot(command_prefix='/', intents=intents)


@client.event
async def on_ready():
    print("The bot is now ready to use")


@client.command()
async def hello(ctx):
    await ctx.send("Hello, I am the bot!!!")


@client.event
async def on_member_join(member):
    # Get the channel where you want to send the welcome message
    channel = discord.utils.get(member.guild.channels, name='welcome')

    if channel is not None:
        try:
            # Send a welcome message in the specified channel
            await channel.send(f"Welcome {member.mention} to the server! Have a Good Day:)")

            # Initiate a direct message to the new member
            await member.send("Welcome to the server!Have a Good Day:)")
        except Exception as e:
            print(f"An error occurred: {e}")


client.run(BOT_TOKEN)
