# key_alive.py
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Alive ✅"

def keep_alive():
    thread = threading.Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 8080})
    thread.start()
