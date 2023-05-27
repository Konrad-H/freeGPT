import os
import openai
import discord
from discord.ext import commands

from chat_assistant import ChatAssistant

with  open("discord.token") as f:
    DISCORD_TOKEN = f.readline() # Replace this with your actual bot token
with  open("openai.token") as f:
    OPENAI_TOKEN = f.readline() # Replace this with your actual bot token
print(DISCORD_TOKEN)

INPUT_PROMPT = "You are Free-petto, a helpful assistant! Your name is (a play on the words GPT (the model that powers your) or Gepetto in italian, and free, because you are and will always be free)"

CONVERSATION_HISTORY = []

intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False
client = commands.Bot(command_prefix="", intents=intents)  # Empty prefix

assistant = ChatAssistant(OPENAI_TOKEN)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    response_text = await assistant.generate_chat_response(message.content)
    await message.channel.send(response_text)

client.run(DISCORD_TOKEN)