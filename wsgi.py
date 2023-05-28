from flask import Flask
from threading import Thread
from app import run_discord_bot

app = Flask(__name__)

@app.route('/')
def hello():
    return f'Hello, Your Discord bot is running!'


if __name__ == '__main__':

    bot_thread = Thread(target=run_discord_bot)
    bot_thread.start()

    app.run()