from flask import Flask, request, redirect, render_template
import sqlite3
import random
import string

app = Flask(__name__)

# Create Database
def init_db():
    conn = sqlite3.connect('urls.db')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS urls(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        short_code TEXT UNIQUE,
        long_url TEXT
    )
    ''')

    conn.commit()
    conn.close()

# Generate Short Code
def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/')
def home():
    return render_template('index.html')

# API to shorten URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form['long_url']

    short_code = generate_code()

    conn = sqlite3.connect('urls.db')
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO urls(short_code, long_url) VALUES (?, ?)",
        (short_code, long_url)
    )

    conn.commit()
    conn.close()

    short_url = request.host_url + short_code

    return f"Short URL: <a href='{short_url}'>{short_url}</a>"

# Redirect Route
@app.route('/<short_code>')
def redirect_url(short_code):
    conn = sqlite3.connect('urls.db')
    cur = conn.cursor()

    cur.execute(
        "SELECT long_url FROM urls WHERE short_code=?",
        (short_code,)
    )

    result = cur.fetchone()
    conn.close()

    if result:
        return redirect(result[0])

    return "URL not found", 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)