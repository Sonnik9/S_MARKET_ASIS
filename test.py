# top_coins = ['dfkjbvk', 'skdfhbv']
# response_message = str(top_coins)[1:-1].replace(',', '').replace("'", '')
# print(response_message)

# top_coins = ['dfkjbvk', 'skdfhbv', 'dfkjbvk', 'skdfhbv']
# # response_message = str(top_coins)[2:-2].replace("', '", ', ')
# response_message = ', '.join(top_coins)
# print(response_message)

# import requests
# from datetime import datetime
# import pandas as pd
# import asyncio
# import time
# from connectorss import CONNECTOR_TG

# class GETT_API_TEST(CONNECTOR_TG):

#     def __init__(self) -> None:
#         super().__init__()  

# # ///////////////////////////////////////////////////////////////////
#     def get_current_price(self, symbol):
#         method = 'GET'
#         data = None
#         current_price = None
#         url =  f'https://api.binance.com/api/v3/allOrders'
#         params = {'symbol': symbol}
#         print(f"symbol: {symbol}")
#         try:
#             params = self.get_signature(params)
#             data = self.HTTP_request(url, method=method, params=params) 
#             print(data)  
#             # current_price = float([x['price'] for x in current_price if x['symbol'] == symbol])
            
#         except Exception as ex:
#             print(ex)
#         return current_price  

# get_data = GETT_API_TEST()
# symbol="BTCUSDT"
# data = get_data.get_current_price(symbol)
# print(data)

# depo = '12usdt'
# depo = '0.02BTC'
# depo = depo.upper()
# symbol = 'BTC'

# depo = depo.upper()
# if depo.upper().endswith('USDT'):
#     depo = float(depo.replace('USDT', '').strip())
#     print(depo*2)
# if depo.upper().endswith(f'{symbol}'):
#     depo = '0.02btc'
#     depo = depo.upper()
#     depo = float(depo.replace(f'{symbol}', '').strip())
#     print(depo*2)



# [{'info': {'symbol': 'BTCUSDT', 'id': '3354245261', 'orderId': '24101115750', 'orderListId': '-1', 'price': '43397.01000000', 'qty': '0.00230000', 'quoteQty': '99.81312300', 'commission': '0.00000230', 'commissionAsset': 'BTC', 'time': '1704475420512', 'isBuyer': True, 'isMaker': False, 'isBestMatch': True}, 'timestamp': 1704475420512, 'datetime': '2024-01-05T17:23:40.512Z', 'symbol': 'BTC/USDT', 'id': '3354245261', 'order': '24101115750', 'type': None, 'side': 'buy', 'takerOrMaker': 'taker', 'price': 43397.01, 'amount': 0.0023, 'cost': 99.813123, 'fee': {'cost': 2.3e-06, 'currency': 'BTC'}, 'fees': [{'cost': 2.3e-06, 'currency': 'BTC'}]}, {'info': {'symbol': 'BTCUSDT', 'id': '3354290652', 'orderId': '24101461126', 'orderListId': '-1', 'price': '43600.00000000', 'qty': '0.00229000', 'quoteQty': '99.84400000', 'commission': '0.09984400', 'commissionAsset': 'USDT', 'time': '1704477256789', 'isBuyer': False, 'isMaker': True, 'isBestMatch': True}, 'timestamp': 1704477256789, 'datetime': '2024-01-05T17:54:16.789Z', 'symbol': 'BTC/USDT', 'id': '3354290652', 'order': '24101461126', 'type': None, 'side': 'sell', 'takerOrMaker': 'maker', 'price': 43600.0, 'amount': 0.00229, 'cost': 99.844, 'fee': {'cost': 0.099844, 'currency': 'USDT'}, 'fees': [{'cost': 0.099844, 'currency': 'USDT'}]}, {'info': {'symbol': 'BTCUSDT', 'id': '3355192121', 'orderId': '24112743379', 'orderListId': '-1', 'price': '43655.99000000', 'qty': '0.00200000', 'quoteQty': '87.31198000', 'commission': '0.00000200', 'commissionAsset': 'BTC', 'time': '1704541911911', 'isBuyer': True, 'isMaker': False, 'isBestMatch': True}, 'timestamp': 1704541911911, 'datetime': '2024-01-06T11:51:51.911Z', 'symbol': 'BTC/USDT', 'id': '3355192121', 'order': '24112743379', 'type': None, 'side': 'buy', 'takerOrMaker': 'taker', 'price': 43655.99, 'amount': 0.002, 'cost': 87.31198, 'fee': {'cost': 2e-06, 'currency': 'BTC'}, 'fees': [{'cost': 2e-06, 'currency': 'BTC'}]}, {'info': {'symbol': 'BTCUSDT', 'id': '3355274353', 'orderId': '24113636125', 'orderListId': '-1', 'price': '43800.00000000', 'qty': '0.00200000', 'quoteQty': '87.60000000', 'commission': '0.08760000', 'commissionAsset': 'USDT', 'time': '1704550342616', 'isBuyer': False, 'isMaker': True, 'isBestMatch': True}, 'timestamp': 1704550342616, 'datetime': '2024-01-06T14:12:22.616Z', 'symbol': 'BTC/USDT', 'id': '3355274353', 'order': '24113636125', 'type': None, 'side': 'sell', 'takerOrMaker': 'maker', 'price': 43800.0, 'amount': 0.002, 'cost': 87.6, 'fee': {'cost': 0.0876, 'currency': 'USDT'}, 'fees': [{'cost': 0.0876, 'currency': 'USDT'}]}, {'info': {'symbol': 'BTCUSDT', 'id': '3357144602', 'orderId': '24134151230', 'orderListId': '-1', 'price': '44000.00000000', 'qty': '0.00110000', 'quoteQty': '48.40000000', 'commission': '0.04840000', 'commissionAsset': 'USDT', 'time': '1704694899111', 'isBuyer': False, 'isMaker': True, 'isBestMatch': True}, 'timestamp': 1704694899111, 'datetime': '2024-01-08T06:21:39.111Z', 'symbol': 'BTC/USDT', 'id': '3357144602', 'order': '24134151230', 'type': None, 'side': 'sell', 'takerOrMaker': 'maker', 'price': 44000.0, 'amount': 0.0011, 'cost': 48.4, 'fee': {'cost': 0.0484, 'currency': 'USDT'}, 'fees': [{'cost': 0.0484, 'currency': 'USDT'}]}, {'info': {'symbol': 'BTCUSDT', 'id': '3361635051', 'orderId': '24183405461', 'orderListId': '-1', 'price': '45970.61000000', 'qty': '0.00400000', 'quoteQty': '183.88244000', 'commission': '0.00000400', 'commissionAsset': 'BTC', 'time': '1704839833195', 'isBuyer': True, 'isMaker': False, 'isBestMatch': True}, 'timestamp': 1704839833195, 'datetime': '2024-01-09T22:37:13.195Z', 'symbol': 'BTC/USDT', 'id': '3361635051', 'order': '24183405461', 'type': None, 'side': 'buy', 'takerOrMaker': 'taker', 'price': 45970.61, 'amount': 0.004, 'cost': 183.88244, 'fee': {'cost': 4e-06, 'currency': 'BTC'}, 'fees': [{'cost': 4e-06, 'currency': 'BTC'}]}, {'info': {'symbol': 'BTCUSDT', 'id': '3363351202', 'orderId': '24202918703', 'orderListId': '-1', 'price': '45457.98000000', 'qty': '0.00200000', 'quoteQty': '90.91596000', 'commission': '0.00000200', 'commissionAsset': 'BTC', 'time': '1704904846773', 'isBuyer': True, 'isMaker': False, 'isBestMatch': True}, 'timestamp': 1704904846773, 'datetime': '2024-01-10T16:40:46.773Z', 'symbol': 'BTC/USDT', 'id': '3363351202', 'order': '24202918703', 'type': None, 'side': 'buy', 'takerOrMaker': 'taker', 'price': 45457.98, 'amount': 0.002, 'cost': 90.91596, 'fee': {'cost': 2e-06, 'currency': 'BTC'}, 'fees': [{'cost': 2e-06, 'currency': 'BTC'}]}, {'info': {'symbol': 'BTCUSDT', 'id': '3363411408', 'orderId': '24202947705', 'orderListId': '-1', 'price': '45700.00000000', 'qty': '0.00200000', 'quoteQty': '91.40000000', 'commission': '0.09140000', 'commissionAsset': 'USDT', 'time': '1704907768487', 'isBuyer': False, 'isMaker': True, 'isBestMatch': True}, 'timestamp': 1704907768487, 'datetime': '2024-01-10T17:29:28.487Z', 'symbol': 'BTC/USDT', 'id': '3363411408', 'order': '24202947705', 'type': None, 'side': 'sell', 'takerOrMaker': 'maker', 'price': 45700.0, 'amount': 0.002, 'cost': 91.4, 'fee': {'cost': 0.0914, 'currency': 'USDT'}, 'fees': [{'cost': 0.0914, 'currency': 'USDT'}]}, {'info': {'symbol': 'BTCUSDT', 'id': '3363624539', 'orderId': '24205503350', 'orderListId': '-1', 'price': '46500.00000000', 'qty': '0.00200000', 'quoteQty': '93.00000000', 'commission': '0.09300000', 'commissionAsset': 'USDT', 'time': '1704911445092', 'isBuyer': False, 'isMaker': True, 'isBestMatch': True}, 'timestamp': 1704911445092, 'datetime': '2024-01-10T18:30:45.092Z', 'symbol': 'BTC/USDT', 'id': '3363624539', 'order': '24205503350', 'type': None, 'side': 'sell', 'takerOrMaker': 'maker', 'price': 46500.0, 'amount': 0.002, 'cost': 93.0, 'fee': {'cost': 0.093, 'currency': 'USDT'}, 'fees': [{'cost': 0.093, 'currency': 'USDT'}]}, {'info': {'symbol': 'BTCUSDT', 'id': '3364667425', 'orderId': '24205485949', 'orderListId': '-1', 'price': '47000.00000000', 'qty': '0.00200000', 'quoteQty': '94.00000000', 'commission': '0.09400000', 'commissionAsset': 'USDT', 'time': '1704927920102', 'isBuyer': False, 'isMaker': True, 'isBestMatch': True}, 'timestamp': 1704927920102, 'datetime': '2024-01-10T23:05:20.102Z', 'symbol': 'BTC/USDT', 'id': '3364667425', 'order': '24205485949', 'type': None, 'side': 'sell', 'takerOrMaker': 'maker', 'price': 47000.0, 'amount': 0.002, 'cost': 94.0, 'fee': {'cost': 0.094, 'currency': 'USDT'}, 'fees': [{'cost': 0.094, 'currency': 'USDT'}]}, {'info': {'symbol': 'BTCUSDT', 'id': '3367767910', 'orderId': '24243674034', 'orderListId': '-1', 'price': '46187.59000000', 'qty': '0.00200000', 'quoteQty': '92.37518000', 'commission': '0.00000200', 'commissionAsset': 'BTC', 'time': '1705009650525', 'isBuyer': True, 'isMaker': False, 'isBestMatch': True}, 'timestamp': 1705009650525, 'datetime': '2024-01-11T21:47:30.525Z', 'symbol': 'BTC/USDT', 'id': '3367767910', 'order': '24243674034', 'type': None, 'side': 'buy', 'takerOrMaker': 'taker', 'price': 46187.59, 'amount': 0.002, 'cost': 92.37518, 'fee': {'cost': 2e-06, 'currency': 'BTC'}, 'fees': [{'cost': 2e-06, 'currency': 'BTC'}]}, {'info': {'symbol': 'BTCUSDT', 'id': '3373237851', 'orderId': '24308278354', 'orderListId': '-1', 'price': '42159.99000000', 'qty': '0.00100000', 'quoteQty': '42.15999000', 'commission': '0.00000100', 'commissionAsset': 'BTC', 'time': '1705271717476', 'isBuyer': True, 'isMaker': False, 'isBestMatch': True}, 'timestamp': 1705271717476, 'datetime': '2024-01-14T22:35:17.476Z', 'symbol': 'BTC/USDT', 'id': '3373237851', 'order': '24308278354', 'type': None, 'side': 'buy', 'takerOrMaker': 'taker', 'price': 42159.99, 'amount': 0.001, 'cost': 42.15999, 'fee': {'cost': 1e-06, 'currency': 'BTC'}, 'fees': [{'cost': 1e-06, 'currency': 'BTC'}]}, {'info': {'symbol': 'BTCUSDT', 'id': '3374467713', 'orderId': '24308302930', 'orderListId': '-1', 'price': '43000.00000000', 'qty': '0.00100000', 'quoteQty': '43.00000000', 'commission': '0.04300000', 'commissionAsset': 'USDT', 'time': '1705343153033', 'isBuyer': False, 'isMaker': True, 'isBestMatch': True}, 'timestamp': 1705343153033, 'datetime': '2024-01-15T18:25:53.033Z', 'symbol': 'BTC/USDT', 'id': '3374467713', 'order': '24308302930', 'type': None, 'side': 'sell', 'takerOrMaker': 'maker', 'price': 43000.0, 'amount': 0.001, 'cost': 43.0, 'fee': {'cost': 0.043, 'currency': 'USDT'}, 'fees': [{'cost': 0.043, 'currency': 'USDT'}]}, {'info': {'symbol': 'BTCUSDT', 'id': '3381894408', 'orderId': '24421604067', 'orderListId': '-1', 'price': '41550.93000000', 'qty': '0.00029000', 'quoteQty': '12.04976970', 'commission': '0.00000029', 'commissionAsset': 'BTC', 'time': '1705772569051', 'isBuyer': True, 'isMaker': False, 'isBestMatch': True}, 'timestamp': 1705772569051, 'datetime': '2024-01-20T17:42:49.051Z', 'symbol': 'BTC/USDT', 'id': '3381894408', 'order': '24421604067', 'type': None, 'side': 'buy', 'takerOrMaker': 'taker', 'price': 41550.93, 'amount': 0.00029, 'cost': 12.0497697, 'fee': {'cost': 2.9e-07, 'currency': 'BTC'}, 'fees': [{'cost': 2.9e-07, 'currency': 'BTC'}]}, {'info': {'symbol': 'BTCUSDT', 'id': '3381900662', 'orderId': '24421674892', 'orderListId': '-1', 'price': '41589.99000000', 'qty': '0.00029000', 'quoteQty': '12.06109710', 'commission': '0.01206110', 'commissionAsset': 'USDT', 'time': '1705773298891', 'isBuyer': False, 'isMaker': False, 'isBestMatch': True}, 'timestamp': 1705773298891, 'datetime': '2024-01-20T17:54:58.891Z', 'symbol': 'BTC/USDT', 'id': '3381900662', 'order': '24421674892', 'type': None, 'side': 'sell', 'takerOrMaker': 'taker', 'price': 41589.99, 'amount': 0.00029, 'cost': 12.0610971, 'fee': {'cost': 0.0120611, 'currency': 'USDT'}, 'fees': [{'cost': 0.0120611, 'currency': 'USDT'}]}, {'info': {'symbol': 'BTCUSDT', 'id': '3381909867', 'orderId': '24421768604', 'orderListId': '-1', 'price': '41528.94000000', 'qty': '0.00024000', 'quoteQty': '9.96694560', 'commission': '0.00000024', 'commissionAsset': 'BTC', 'time': '1705774236202', 'isBuyer': True, 'isMaker': False, 'isBestMatch': True}, 'timestamp': 1705774236202, 'datetime': '2024-01-20T18:10:36.202Z', 'symbol': 'BTC/USDT', 'id': '3381909867', 'order': '24421768604', 'type': None, 'side': 'buy', 'takerOrMaker': 'taker', 'price': 41528.94, 'amount': 0.00024, 'cost': 9.9669456, 'fee': {'cost': 2.4e-07, 'currency': 'BTC'}, 'fees': [{'cost': 2.4e-07, 'currency': 'BTC'}]}, {'info': {'symbol': 'BTCUSDT', 'id': '3381916218', 'orderId': '24421819384', 'orderListId': '-1', 'price': '41549.67000000', 'qty': '0.00029000', 'quoteQty': '12.04940430', 'commission': '0.01204940', 'commissionAsset': 'USDT', 'time': '1705774638139', 'isBuyer': False, 'isMaker': False, 'isBestMatch': True}, 'timestamp': 1705774638139, 'datetime': '2024-01-20T18:17:18.139Z', 'symbol': 'BTC/USDT', 'id': '3381916218', 'order': '24421819384', 'type': None, 'side': 'sell', 'takerOrMaker': 'taker', 'price': 41549.67, 'amount': 0.00029, 'cost': 12.0494043, 'fee': {'cost': 0.0120494, 'currency': 'USDT'}, 'fees': [{'cost': 0.0120494, 'currency': 'USDT'}]}, {'info': {'symbol': 'BTCUSDT', 'id': '3381919667', 'orderId': '24421877188', 'orderListId': '-1', 'price': '41608.00000000', 'qty': '0.00029000', 'quoteQty': '12.06632000', 'commission': '0.00000029', 'commissionAsset': 'BTC', 'time': '1705775204887', 'isBuyer': True, 'isMaker': False, 'isBestMatch': True}, 'timestamp': 1705775204887, 'datetime': '2024-01-20T18:26:44.887Z', 'symbol': 'BTC/USDT', 'id': '3381919667', 'order': '24421877188', 'type': None, 'side': 'buy', 'takerOrMaker': 'taker', 'price': 41608.0, 'amount': 0.00029, 'cost': 12.06632, 'fee': {'cost': 2.9e-07, 'currency': 'BTC'}, 'fees': [{'cost': 2.9e-07, 'currency': 'BTC'}]}, {'info': {'symbol': 'BTCUSDT', 'id': '3381924283', 'orderId': '24421931230', 'orderListId': '-1', 'price': '41623.65000000', 'qty': '0.00024000', 'quoteQty': '9.98967600', 'commission': '0.00998968', 'commissionAsset': 'USDT', 'time': '1705775826640', 'isBuyer': False, 'isMaker': False, 'isBes


# import time
# from datetime import datetime


# cur_time = datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
# print(cur_time)


# import logging, os, inspect

# logging.basicConfig(filename='config_log.log', level=logging.INFO)
# current_file = os.path.basename(__file__)

# try:
#     a = 'sfk'
#     b = int(a)
#     print(b)

# except Exception as ex:
#     logging.exception(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

# message = 'btc 12usdt/45000 15usdt/47100'   

# target_prices = message.strip().split(' ')
# symbol = target_prices[0]
# print(symbol)
# print(target_prices[1:])

