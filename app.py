import sqlite3

import click
from flask import Flask, g, render_template, current_app
from flask.cli import with_appcontext

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('Apifiles\APIandOutput\capstonedatabase.sqlite')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def messario_api():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM messario_news').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)
