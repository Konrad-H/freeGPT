from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return f'Hello, Your Discord bot is running!'

if __name__ == '__main__':
    app.run()