from chalice import Chalice
from binance.client import Client
from binance.enums import *
from decimal import *
import time, json
from chalicelib import config

USD_amount = 300

client = Client(config.API_KEY, config.API_SECRET, tld='us')

app = Chalice(app_name='bin02')

@app.route('/')
def index():
    return {'hello': 'world'}

@app.route('/order02', methods=['POST'])
def order02():
    request = app.current_request
    webhook_message = request.json_body
   
    if webhook_message['side'] == "buy":
        quantity = Decimal(USD_amount/webhook_message['close'])
        rounded = round(quantity, 3)
        order = client.create_order(
            symbol=webhook_message['ticker'],
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            quantity=rounded
            )
        
    else:
        coin = webhook_message['ticker']
        size = len(coin)
        mod_string = coin[:size - 3]
        #load the data into an element
        balance = client.get_asset_balance(asset=mod_string)

        #dumps the json object into an element
        data = json.dumps(balance)

        #load the json to a string
        resp = json.loads(data)

        order = client.create_order(
            symbol=webhook_message['ticker'],
            side=SIDE_SELL,
            type=ORDER_TYPE_MARKET,
            quantity=resp['free'][0:4]
        )

    return {
        'webhook_message': webhook_message
    }
