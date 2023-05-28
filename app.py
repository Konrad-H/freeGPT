import os
import discord
from discord.ext import commands

from chat_assistant import ChatAssistant



try:
    with  open("discord.token") as f:
        DISCORD_TOKEN = f.readline() # Replace this with your actual bot token
    with  open("openai.token") as f:
        OPENAI_API_KEY = f.readline() # Replace this with your actual bot token
    print("env variables found in folder")
except:
    DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

INPUT_PROMPT = "You are Free-petto, a helpful assistant! Your name is (a play on the words GPT (the model that powers your) or Gepetto in italian, and free, because you are and will always be free)"

CONVERSATION_HISTORY = []

intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False
client = commands.Bot(command_prefix="", intents=intents)  # Empty prefix

assistant = ChatAssistant(OPENAI_API_KEY, input_prompt=INPUT_PROMPT)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    print("MESSAGE RECIEVED")
    if message.author == client.user:
        return
    print("MESSAGE SENT")
    response_text = await assistant.generate_chat_response(message.content)
    await message.channel.send(response_text)

def run_discord_bot():
    print("Bot ready to start")
    client.run(DISCORD_TOKEN)
    
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/healthz', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

def run_flask_app():
    app.run(host="0.0.0.0", port=8080)


if __name__ == '__main__':
    from threading import Thread
    Thread(target=run_flask_app).start()
    run_discord_bot()