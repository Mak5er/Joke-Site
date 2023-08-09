import os
import random
import sqlite3
import time

import requests
from urllib.parse import quote
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

load_dotenv()

bot_api_url = os.getenv("bot_api_url")
chat_id = os.getenv("chat_id")


# Конфігурація основних кольорів


# Функція для отримання рандомного анекдоту з бази даних
def get_random_joke():
    with sqlite3.connect('jokes.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT text FROM jokes_uk')
        jokes = cursor.fetchall()

    if jokes:
        random_joke = random.choice(jokes)[0]
        return random_joke
    else:
        return "У базі даних немає анекдотів."


@app.route('/', methods=['GET', 'POST'])
def index():
    random_joke = get_random_joke()
    return render_template('index.html', random_joke=random_joke)


last_request_time = 0


@app.route('/get_random_joke', methods=['POST'])
def get_random_joke_ajax():
    global last_request_time
    current_time = time.time()

    if current_time - last_request_time >= 1:  # Перевірка, чи пройшла 1 секунда з останнього запиту
        last_request_time = current_time  # Оновлюємо час останнього запиту
        random_joke = get_random_joke()
        return jsonify(random_joke)
    else:
        pass


@app.route('/send_idea', methods=['POST'])
def send_idea():
    idea = request.form['idea']
    encoded_idea = quote(idea)
    message = f'/sendMessage?chat_id={chat_id}&text=*Нова ідея*: \n`{encoded_idea}`&parse_mode=MarkdownV2'
    response = requests.get(bot_api_url + message)
    print(response.json())
    return 'Idea sent!'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
