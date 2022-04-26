import json
import sqlite3
import click
import plotly
from flask import Flask, g, render_template, current_app
from flask.cli import with_appcontext
from flask_navigation import Navigation
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import plotly.graph_objects as go

app = Flask(__name__)
nav = Navigation(app)

nav.Bar('top', [
    nav.Item('Home', 'home'),
    nav.Item('News', 'messario_news'),
    nav.Item('Candles', 'finnhub_candles'),
    nav.Item('Coin Market', 'coinlore_coin_market'),
    nav.Item('Trade Assets', 'trade_assets'),
    nav.Item('Coin Info', 'cryptocompare_coin_info'),
])


def get_db_connection():
    conn = sqlite3.connect('Apifiles\APIandOutput\capstonedatabase.sqlite')
    conn.row_factory = sqlite3.Row
    return conn


def create_plot():
    conn = get_db_connection()
    df = pd.read_sql_query('SELECT * FROM finnhub_candles', conn)
    fig = go.Figure(
        data=[go.Candlestick(
            x=df['tstamp'],
            open=df['open_price'],
            high=df['high_price'],
            low=df['low_price'],
            close=df['close_price']
        )]
    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

# Call/Collect data from all database tables
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/news')
def messario_news():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM messario_news').fetchall()
    conn.close()
    return render_template('news.html', posts=posts)


@app.route('/coin_info')
def cryptocompare_coin_info():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM cryptocompare_coin_info').fetchall()
    conn.close()
    return render_template('coin_info.html', posts=posts)


@app.route('/candles')
def finnhub_candles():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM finnhub_candles').fetchall()
    bar = create_plot()
    conn.close()
    return render_template('candles.html', posts=posts, plot=bar)


@app.route('/coin_market')
def coinlore_coin_market():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM coinlore_coin_market').fetchall()
    conn.close()
    return render_template('coin_market.html', posts=posts)


@app.route('/assets')
def trade_assets():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM trade_assets').fetchall()
    conn.close()
    return render_template('assets.html', posts=posts)
