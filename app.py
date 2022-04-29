import json
import sqlite3
import plotly
from flask import Flask, g, render_template
from flask_navigation import Navigation
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc
from dash import html

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
    df = pd.read_sql_query('SELECT * FROM finnhub_candles', conn)

    fig = go.Figure(data=[go.Candlestick(x=df['tstamp'],
        open=df['open_price'],
        high=df['high_price'],
        low=df['low_price'],
        close=df['close_price'])])

    #include a go.Bar trace for volumes
    fig.add_trace(go.Bar(x=df['tstamp'], y=df['volume_data']), secondary_y=False)
    fig.layout.yaxis2.showgrid = False
    data = [fig]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    conn.close()
    return render_template('candles.html', graphJSON=graphJSON)


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
