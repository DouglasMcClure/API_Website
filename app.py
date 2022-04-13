import sqlite3

import click
from flask import Flask, g, render_template, current_app
from flask.cli import with_appcontext

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('Apifiles\APIandOutput\capstonedatabase.sqlite')
    conn.row_factory = sqlite3.Row
    return conn


# Call/Collect data from all database tables
@app.route('/')
def messario_news():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM messario_news').fetchall()
    conn.close()
    return render_template('news.html', posts=posts)


def cryptocompare_coin_info():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM cryptocompare_coin_info').fetchall()
    conn.close()
    return render_template('coin_info.html', posts=posts)


def finnhub_candles():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM finnhub_candles').fetchall()
    conn.close()
    return render_template('candles.html', posts=posts)


def coinlore_coin_market():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM coinlore_coin_market').fetchall()
    conn.close()
    return render_template('coin_market.html', posts=posts)


def trade_assets():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM trade_assets').fetchall()
    conn.close()
    return render_template('assets.html', posts=posts)
