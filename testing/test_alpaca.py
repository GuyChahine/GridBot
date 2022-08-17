import json

with open('alpaca_key.json') as f:
    keys = json.load(f)

from time import sleep
from alpaca.data import CryptoDataStream

stream = CryptoDataStream(
    api_key=keys['key_id'],
    secret_key=keys['secret_key'],
    )

async def quote_data_handler(data):
    print(data)
    sleep(1)
    
stream.subscribe_quotes(quote_data_handler, "BTCUSD")

stream.run()