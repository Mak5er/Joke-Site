from flask import Flask, render_template, jsonify
import sqlite3
import random

app = Flask(__name__)

# Конфігурація основних кольорів
primary_color = "#3bd671"
background_color = "#212937"


# Функція для отримання рандомного анекдоту з бази даних
def get_random_joke():
    conn = sqlite3.connect('jokes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT text FROM jokes_uk')
    jokes = cursor.fetchall()
    conn.close()

    if jokes:
        random_joke = random.choice(jokes)[0]
        return random_joke
    else:
        return "У базі даних немає анекдотів."


@app.route('/', methods=['GET', 'POST'])
def index():
    random_joke = get_random_joke()
    return render_template('index.html', random_joke=random_joke, primary_color=primary_color,
                           background_color=background_color)


@app.route('/get_random_joke', methods=['POST'])
def get_random_joke_ajax():
    random_joke = get_random_joke()
    return jsonify(random_joke)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
