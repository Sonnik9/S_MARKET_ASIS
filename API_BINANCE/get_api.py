# import time
# import random
from datetime import datetime
import pandas as pd
import asyncio
import time
from connectorss import CONNECTOR_TG
import csv
import json

import logging, os, inspect

logging.basicConfig(filename='config_log.log', level=logging.INFO)
current_file = os.path.basename(__file__)


method = 'GET'

class GETT_API_CCXT(CONNECTOR_TG):
    def __init__(self):   
        super().__init__()

    # def format_and_write_trades_json(self, data, symbol):
        
    #     output_file=f'{symbol}_tradesBook.json'
    #     sorted_data = sorted(data, key=lambda x: x['timestamp'])

    #     # Создание и запись в файл
    #     formatted_trades = []

    #     for trade in sorted_data:
    #         ticker = trade['symbol']
    #         timestamp_ms = trade['timestamp']
    #         date = datetime.utcfromtimestamp(timestamp_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')
    #         amount = trade['amount']
    #         usdt_amount = trade['cost']
    #         side = 'Buy' if trade['side'] == 'buy' else 'Sell'
    #         price = trade['price']
    #         commission = trade['fee']['cost']

    #         # Формирование словаря
    #         formatted_trade = {
    #             'Ticker': ticker,
    #             'Date': date,
    #             'Amount': amount,
    #             'USDT Amount': usdt_amount,
    #             'Commission': commission,
    #             'Side': side,
    #             'Price': price
    #         }

    #         formatted_trades.append(formatted_trade)

    #     with open(output_file, 'w') as json_file:
    #         json.dump(formatted_trades, json_file, indent=2)

    # def format_and_write_trades(self, data, symbol):
    #     output_file = f'{symbol}_tradesBook.csv'
    #     sorted_data = sorted(data, key=lambda x: x['timestamp'])

    #     with open(output_file, mode='w', newline='') as file:
    #         writer = csv.writer(file)
    #         writer.writerow(['Ticker', 'Date', 'Amount', 'USDT Amount', 'Commission', 'Side', 'Price'])

    #         for trade in sorted_data:
    #             ticker = trade['symbol']
    #             timestamp_ms = trade['timestamp']
    #             date = datetime.utcfromtimestamp(timestamp_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')
    #             amount = trade['amount']
    #             usdt_amount = trade['cost']
    #             side = 'Buy' if trade['side'] == 'buy' else 'Sell'
    #             price = trade['price']
    #             commission = trade['fee']['cost']
    #             writer.writerow([ticker, date, amount, usdt_amount, commission, side, price])

    def calculate_profit_and_balance_json(self, data):

        
        sorted_data = sorted(data, key=lambda x: x['timestamp'])

        formatted_trades = []

        # Переменные для бухгалтерских расчетов
        total_buy_amount = 0
        total_buy_cost = 0
        average_buy_price = 0
        total_profit = 0
        balance = 0
        total_balance = ''
       

        for i, trade in enumerate(sorted_data):
            profit = 0
            ticker = trade['symbol']
            timestamp_ms = trade['timestamp']
            date = datetime.utcfromtimestamp(timestamp_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')
            amount = trade['amount']
            usdt_amount = trade['cost']
            side = 'Buy' if trade['side'] == 'buy' else 'Sell'
            price = trade['price']
            commission = trade['fee']['cost']

            if side == 'Buy':
                total_buy_amount += amount
                balance += amount
                total_buy_cost += usdt_amount
                average_buy_price = total_buy_cost / total_buy_amount

            elif side == 'Sell':
                profit = (amount * price) - commission - (amount * average_buy_price)
                balance -= amount

            if profit !=0:
                total_profit += profit
            else:
                profit = ''

            if i == len(sorted_data) - 1:
                total_balance = balance 
                total_total_profit = total_profit
            else:
                total_balance = ''
                total_total_profit = ''


            if balance >0:
                formatted_trade = {
                    'Ticker': ticker,
                    'Date': date,
                    'Amount': amount,
                    'USDT Amount': usdt_amount,
                    'Commission': commission,
                    'Side': side,
                    'Price': price,
                    'Profit': profit,
                    'Total_profit': total_total_profit,
                    'Balance': total_balance
                }
                formatted_trades.append(formatted_trade)
            else:
                # balance += amount
                pass


        return formatted_trades






    def get_myBook(self, symbol):
        formatted_trades = None
        try:
            self.exchange.fetch_total_balance()
            trades_data = self.exchange.fetch_my_trades(symbol)
            # self.format_and_write_trades(trades_data, symbol)
            # self.format_and_write_trades_json(trades_data, symbol)
            formatted_trades = self.calculate_profit_and_balance_json(trades_data)
            output_file=f'{symbol}_tradesBook.json'
            with open(output_file, 'w') as json_file:
                json.dump(formatted_trades, json_file, indent=2)
            
            return True
        except Exception as ex:
            logging.exception(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

        return False
        

    def get_ccxtBinance_balance(self):       
        bal = None
        retry_number = 3
        decimal = 1.1        
        for i in range(retry_number):
            try:
                bal = self.exchange.fetch_total_balance()
                if bal:
                    bal = [f"{key}: {value}" for key, value in bal.items() if float(value) !=0]
                if bal:
                    bal = '\n'.join(bal)
                    return bal
                return "Balance==0"
            except Exception as ex:
                logging.exception(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
                time.sleep(1.1 + i*decimal)     

        return "Some problem with fetching balance..."

    def get_ccxtBinance_klines(self, symbol, timeframe, limit):

        retry_number = 3
        decimal = 1.1        
        for i in range(retry_number):
            try:
                klines = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)                
                data = pd.DataFrame(klines, columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
                data['Time'] = pd.to_datetime(data['Time'], unit='ms')
                data.set_index('Time', inplace=True)
                data = data.astype(float)
                return data
            except Exception as e:
                print(f"Error fetching klines: {e}")
                # time.sleep(1)
                time.sleep(1.1 + i*decimal)     

        return pd.DataFrame()

    # def get_ccxtBinance_curPrice(self, symbol):
    #     retry_number = 3
    #     decimal = 1.1  
    #     print(symbol)  
    # #    symbol = 'BNB/USDT'    
    #     for i in range(retry_number):
    #         try:
    #             ticker = self.exchange.fetch_ticker(symbol)
    #             last_price = ticker['last']                
    #             return last_price
    #         except Exception as e:
    #             print(f"Error fetching ticker: {e}")
    #             time.sleep(1.1 + i * decimal)     

    #     return 'Some problems with fetching last price'
    
    # def transformed_qnt(self, symbol, amount):
        
    #     self.exchange.load_markets()
    #     formatted_amount = self.exchange.amount_to_precision(symbol, amount)
    #     return formatted_amount

    # def transformed_price(self, symbol, price):
        
    #     self.exchange.load_markets()
    #     formatted_price = self.exchange.price_to_precision(symbol, price)
    #     return formatted_price

class GETT_API(GETT_API_CCXT):

    def __init__(self) -> None:
        super().__init__()   
        
    def get_all_tickers(self):

        all_tickers = None
        url = self.URL_PATTERN_DICT['all_tikers_url']        
        all_tickers = self.HTTP_request(url, method=method, headers=self.header)

        return all_tickers
    
    def get_excangeInfo(self, symbol):  

        exchangeInfo = None
        if symbol:            
            url = f"{self.URL_PATTERN_DICT['exchangeInfo_url']}?symbol={symbol}"
        else:
            url = self.URL_PATTERN_DICT['exchangeInfo_url']        
        exchangeInfo = self.HTTP_request(url, method=method, headers=self.header)

        return exchangeInfo

    # def get_balance(self):
        
    #     bal = None
    #     retry_number = 3
    #     decimal = 1.1     
        
    #     url = self.URL_PATTERN_DICT['balance_url']        
    #     params = {}
    #     params['recvWindow'] = 5000   
    #     for i in range(retry_number):
    #         try:
    #             params = self.get_signature(params)
    #             bal = self.HTTP_request(url, method=method, headers=self.header, params=params)             
    #             bal = bal['balances']        
    #             if bal:
    #                 bal = [f"{x['asset']}: {x['free']}" for x in bal if float(x['free']) != 0]
    #             if bal:
    #                 bal = '\n'.join(bal)
    #                 return bal
    #             return "Balance==0"
    #         except Exception as ex:
    #             logging.exception(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
    #             time.sleep(1.1 + i*decimal)     

    #     return "Some problem with fetching balance..."
    
    
    # ///////////////////////////////////////////////////////////////////
    def get_current_price(self, symbol):
        
        method = 'GET'
        
        current_price = None
        url = self.URL_PATTERN_DICT['current_price_url']
        params = {'symbol': symbol}
        print(f"symbol: {symbol}")
        try:
            current_price = self.HTTP_request(url, method=method, params=params) 
            # print(current_price)  
            # current_price = float([x['price'] for x in current_price if x['symbol'] == symbol])
            current_price = float(current_price["price"])
        except Exception as ex:
            logging.exception(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

        return current_price  

# ///////////////////////////////////////////////////////////////////////////////////////   
        
    def get_DeFacto_price(self, symbol):       
        try:
            positions = None        
            url = self.URL_PATTERN_DICT['positions_url']
            params = {}
            params = self.get_signature(params)
            positions = self.HTTP_request(url, method=method, headers=self.header, params=params)
            print(positions)
            
            positions = float([x for x in positions if x['symbol'] == symbol][0]["entryPrice"])
        except Exception as ex:
            logging.exception(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")


        return positions
    

# # ////////////////////////////////////////////////////////////////////////////////////

    def get_all_orders(self):
        all_orders = None        
        params = {}               
        url = self.URL_PATTERN_DICT['get_all_orders_url']
        params = self.get_signature(params)
        all_orders = self.HTTP_request(url, method=method, headers=self.header, params=params)

        return all_orders
    
# //////////////////////////////////////////////////////////////////////////////////

get_apii = GETT_API()
symbol = 'BTCUSDT'
print(get_apii.get_myBook(symbol))
# symbol = 'BNBUSDT'
# print(get_apii.get_current_price(symbol))
# print(get_apii.get_ccxtBinance_curPrice(symbol))


