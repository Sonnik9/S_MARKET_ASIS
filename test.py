# top_coins = ['dfkjbvk', 'skdfhbv']
# response_message = str(top_coins)[1:-1].replace(',', '').replace("'", '')
# print(response_message)

# top_coins = ['dfkjbvk', 'skdfhbv', 'dfkjbvk', 'skdfhbv']
# # response_message = str(top_coins)[2:-2].replace("', '", ', ')
# response_message = ', '.join(top_coins)
# print(response_message)

import requests
from datetime import datetime
import pandas as pd
import asyncio
import time
from connectorss import CONNECTOR_TG

class GETT_API_TEST(CONNECTOR_TG):

    def __init__(self) -> None:
        super().__init__()  

# ///////////////////////////////////////////////////////////////////
    def get_current_price(self, symbol):
        method = 'GET'
        data = None
        current_price = None
        url =  f'https://api.binance.com/api/v3/allOrders'
        params = {'symbol': symbol}
        print(f"symbol: {symbol}")
        try:
            params = self.get_signature(params)
            data = self.HTTP_request(url, method=method, params=params) 
            print(data)  
            # current_price = float([x['price'] for x in current_price if x['symbol'] == symbol])
            
        except Exception as ex:
            print(ex)
        return current_price  

get_data = GETT_API_TEST()
symbol="BTCUSDT"
data = get_data.get_current_price(symbol)
print(data)



