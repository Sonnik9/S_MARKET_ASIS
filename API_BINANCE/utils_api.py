from API_BINANCE.delete_api import DELETEE_API 
from RISK.tp_sl_1 import RISK_MANAGEMENT
from datetime import datetime
from decimal import Decimal, ROUND_DOWN
import math
import asyncio
import csv
import json
import time
import logging, os, inspect

logging.basicConfig(filename='config_log.log', level=logging.INFO)
current_file = os.path.basename(__file__)

class UTILS_APII(DELETEE_API, RISK_MANAGEMENT):

    def __init__(self) -> None:
        super().__init__()

    def assets_filters(self):
        all_tickers = []
        top_pairs = []
        
        exclusion_contains_list = ['UP', 'DOWN', 'RUB', 'EUR']
        
        all_tickers = self.get_all_tickers()    
        # print(all_tickers[:5])

        try:
            if all_tickers:
                if not self.price_filter_flag:
                    self.MIN_FILTER_PRICE = 0
                    self.MAX_FILTER_PRICE = math.inf                   

                top_pairs = [ticker for ticker in all_tickers if
                                ticker['symbol'].upper().endswith('USDT') and
                                not any(exclusion in ticker['symbol'].upper() for exclusion in exclusion_contains_list) and
                                (float(ticker['lastPrice']) >= self.MIN_FILTER_PRICE) and (
                                        float(ticker['lastPrice']) <= self.MAX_FILTER_PRICE)]

                print(top_pairs[:4])

                top_pairs = sorted(top_pairs, key=lambda x: float(x['quoteVolume']), reverse=True)
                top_pairs = top_pairs[:self.SLICE_VOLUME_PAIRS]

                if self.min_volume_usdtFilter_flag:
                    top_pairs = [x for x in top_pairs if float(x['quoteVolume']) >= self.MIN_VOLUM_USDT]

                if self.slice_volatilyty_flag:
                    top_pairs = sorted(top_pairs, key=lambda x: abs(float(x['priceChangePercent'])), reverse=True)
                    top_pairs = top_pairs[:self.SLICE_VOLATILITY]
                if self.daily_filter_flag:
                    top_pairs = [x for x in top_pairs if float(x['priceChange']) > 0]

                top_pairs = [x['symbol'] for x in top_pairs if x['symbol'] not in self.problem_pairs]

        except Exception as ex:
            logging.exception(
                f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

        return top_pairs
    
    # ///////////////////////////////////////////////////////////////////////////

    def count_multipliter_places(self, number):
        if isinstance(number, (int, float)):
            number_str = str(number)
            if '.' in number_str:
                return len(number_str.split('.')[1])
        return 0 
    
    # def calc_qnt_func(self, symbol, price, depo): 
    #     symbol_info = None
    #     symbol_data = None 
    #     price_precision = None
    #     quantity_precision = None
    #     quantity = None  
    #     notional = None
    #     recalc_depo = None
    #     usdt_flag = False
    #     # min_qnt = None 
    #     if depo.endswith('USDT'):
    #         depo = float(depo.replace('USDT', '').strip())
    #         print(depo*2)
    #         usdt_flag = True
    #     elif depo.endswith(f"{symbol.replace('USDT', '').strip()}"):            
    #         depo = depo.upper()
    #         depo = float(depo.replace(f"{symbol.replace('USDT', '').strip()}", '').strip())
    #         print(depo*2)

    #     # return
        
    #     try:
    #         symbol_info = self.get_excangeInfo(symbol)
    #     except Exception as ex:
    #         logging.exception(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")  

    #     if symbol_info:
    #         try:
    #             symbol_data = next((item for item in symbol_info["symbols"] if item['symbol'] == symbol), None)
    #         except Exception as ex:
    #             logging.exception(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
            
    #     if symbol_data:   
    #         print(symbol_data)   
    #         return      
    #         try:                
    #             tick_size = float(symbol_data['filters'][0]["tickSize"])
    #             price_precision = int(symbol_data['pricePrecision']) 
    #             # print(f"price_precision: {price_precision}")           
    #             quantity_precision = int(symbol_data['quantityPrecision']) 
    #             lot_size_filter = next((item for item in symbol_data['filters'] if item['filterType'] == 'MIN_NOTIONAL'), None)  
    #             notional = float(lot_size_filter.get('notional', None))
    #             print(f"notional: {notional}")
                
    #         except Exception as ex:
    #             logging.exception(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
        
    #         try:
    #             tick_size = self.count_multipliter_places(tick_size)
    #             print(f"tick_size: {tick_size}")
    #         except Exception as ex:
    #             logging.exception(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 
            
    #         try:  
    #             if depo <= notional:
    #                 depo = notional  
    #             quantity = round(depo / price, quantity_precision)
    #             # quantity = round(depo / price, tick_size)
    #             recalc_depo = quantity * price     
    #             print(f"quantity: {quantity}")
    #             # print(f"{symbol}:  {quantity, recalc_depo, price_precision, tick_size}")
    #         except Exception as ex:
    #             logging.exception(f"An error occurred: {ex}")

    #     # return quantity, recalc_depo, price_precision, tick_size
    
    
# ///////////////////////////////////////////////////////////////////////////////////
    def buy_market_order_temp_func(self, item, depo, is_selling):
        itemm = item.copy()        
        symbol = itemm["symbol"]        
        atr = itemm["atr"]
        entry_price = itemm["current_price"]
        enter_deJure_price = itemm["current_price"]
        open_market_order = None

        try:                    
            itemm['qnt'], itemm['recalc_depo'], itemm['price_precision'] = self.calc_qnt_func(symbol, enter_deJure_price, depo)            
        except Exception as ex:
            logging.exception(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
        print(f"{symbol}:\nitemm['qnt']: {itemm['qnt']}") 
        print(f"{symbol}:\nitemm['recalc_depo']: {itemm['recalc_depo']}") 
        print(f"{symbol}:\nitemm['itemm['price_precision']']: {itemm['price_precision']}") 
        if itemm['qnt']:
            
            success_flag = False
            market_type = 'MARKET'
            target_price = None
            try:          
                open_market_order, success_flag = self.make_order(itemm, is_selling, target_price, market_type)
                print(f"open_market_order:  {open_market_order}") 
            except Exception as ex:
                logging.exception(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
            if success_flag: 
                # pass               
                try:
                    
                    itemm["enter_deFacto_price"] = float(open_market_order['fills'][0]['price'])
                    print(f'str73 {symbol}:  {itemm["enter_deFacto_price"]}  (defacto_prtice)')
                    itemm["done_level"] = 1                                        
                except Exception as ex:
                    logging.exception(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}\n{open_market_order}\n{itemm['enter_deFacto_price']}")

        return itemm

    def tp_make_orders(self, symbol, depo, enter_price, target_prices, auto_flag):
        item = {}
        market_type = 'LIMIT'
        is_selling = -1
        tp_price = None 
        success_flag = False
        item["symbol"] = symbol
        
        
        try:           
            success_flag = False   
            tp_ratio = self.TP_rate
            if auto_flag:
                tp_price = self.static_tp_calc(enter_price, tp_ratio)
                print(f"target_price: {tp_price}")  
                target_price = target_prices[0]       
                open_static_tp_order, success_flag = self.make_order(item, is_selling, tp_price, market_type)
                print(f'open_static_tp_order  {open_static_tp_order}')

            if success_flag:                                     
                item["done_level"] = 2     
        except Exception as ex:
            logging.exception(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}\n{open_static_tp_order}")

        return item
    
#     # ///////////////////////////////////////////////////////////////////////////////
#     async def positions_info(self):
#         positions_data = None
#         positions_data = await self.get_open_positions()
#         try:
#             if len(positions_data) != 0:
#                 positions_data = await self.format_positions_data(positions_data)
#             else:
#                 positions_data = []

#         except Exception as ex:
#             logging.exception(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}\n{positions_data}")


#         return positions_data

#     async def format_positions_data(self, positions_data):
#         formatted_data = ""
#         for position in positions_data:
#             formatted_data += f"Symbol: {position['symbol']}\n"
#             formatted_data += f"Position Amount: {position['positionAmt']}\n"
#             formatted_data += f"Entry Price: {position['entryPrice']}\n"
#             formatted_data += f"Break-Even Price: {position['breakEvenPrice']}\n"
#             formatted_data += f"Mark Price: {position['markPrice']}\n"
#             formatted_data += f"Unrealized Profit: {position['unRealizedProfit']}\n"
#             formatted_data += f"Liquidation Price: {position['liquidationPrice']}\n"
#             formatted_data += f"Leverage: {position['leverage']}\n"
#             formatted_data += f"Max Notional Value: {position['maxNotionalValue']}\n"
#             formatted_data += f"Margin Type: {position['marginType']}\n"
#             formatted_data += f"Isolated Margin: {position['isolatedMargin']}\n"
#             formatted_data += f"Auto Add Margin: {position['isAutoAddMargin']}\n"
#             # formatted_data += f"Position Side: {position['positionSide']}\n"
#             formatted_data += f"Notional: {position['notional']}\n"
#             formatted_data += f"Isolated Wallet: {position['isolatedWallet']}\n"
#             formatted_data += f"Update Time: {datetime.utcfromtimestamp(position['updateTime'] / 1000).strftime('%Y-%m-%d %H:%M:%S')}\n"
#             formatted_data += f"Isolated: {position['isolated']}\n"
#             formatted_data += f"ADL Quantile: {position['adlQuantile']}\n\n"

#         return formatted_data.strip()
    
#     # ///////////////////////////////////////////////////////////////////////////////

#     async def close_all_poss(self):
#         positions_data = None
#         cancel_orders_list = []
#         unSuccess_cancel_orders_list = []
#         success_closePosition_list = []
#         problem_closePosition_list = []
#         defender_corrector = 1
#         new_positions_data = []
        
#         positions_data = await self.get_open_positions()
#         print(f"positions_data: {positions_data}")
#         if positions_data:
#            for x in positions_data:
#                 if float(x['positionAmt']) != 0:
#                     if float(x['positionAmt']) > 0:
#                         defender_corrector = 1
#                     else:
#                         defender_corrector = -1
#                 else:
#                     continue

#                 new_positions_data.append({
#                         "symbol": x['symbol'],
#                         "defender": defender_corrector,
#                         "qnt": abs(float(x['positionAmt'])),
#                     })
#         print(f"new_positions_data: {new_positions_data}")
                
#         is_selling = -1
#         target_price = None
#         market_type = 'MARKET'
#         close_resp_flag = False
#         if new_positions_data:
#             for item in new_positions_data:
#                 close_resp_flag = False
#                 try:
#                     _, close_resp_flag = await self.make_order(item, is_selling, target_price, market_type)
#                 except:
#                     pass
#                 if close_resp_flag:
#                     success_closePosition_list.append(item['symbol'])                    
#                 else:
#                     problem_closePosition_list.append(item['symbol'])

#         # if success_closePosition_list and problem_closePosition_list:
#         # cancel_orders_list, unSuccess_cancel_orders_list = await self.cancel_all_orders_for_position(success_closePosition_list)  
#         cancel_orders_list, unSuccess_cancel_orders_list = await self.cancel_order_by_id(success_closePosition_list)
#         # elif success_closePosition_list and not problem_closePosition_list:
#         # cancel_orders_list, unSuccess_cancel_orders_list = await self.cancel_all_open_orders()              

#         return success_closePosition_list, problem_closePosition_list, cancel_orders_list, unSuccess_cancel_orders_list
                
#     async def close_custom_poss(self, symbol):
#         positions_data = None
#         cancel_orders_list = []
#         unSuccess_cancel_orders_list = []
#         success_closePosition_list = []
#         problem_closePosition_list = []
#         defender_corrector = 1
#         new_positions_data = {}
        
#         positions_data = await self.get_open_positions()
#         positions_data = [x for x in positions_data if x["symbol"] == symbol][0]
#         print(f"positions_data: {positions_data}")
#         if positions_data:           
#             if float(positions_data['positionAmt']) != 0:
#                 if float(positions_data['positionAmt']) > 0:
#                     defender_corrector = 1
#                 else:
#                     defender_corrector = -1

#                 new_positions_data = {
#                         "symbol": positions_data['symbol'],
#                         "defender": defender_corrector,
#                         "qnt": abs(float(positions_data['positionAmt'])),
#                     }
#         print(f"new_positions_data: {new_positions_data}")
                
#         is_selling = -1
#         target_price = None
#         market_type = 'MARKET'
#         close_resp_flag = False
#         if new_positions_data:            
#             close_resp_flag = False
#             try:
#                 _, close_resp_flag = await self.make_order(new_positions_data, is_selling, target_price, market_type)
#             except:
#                 pass
#             if close_resp_flag:
#                 success_closePosition_list.append(new_positions_data['symbol'])                    
#             else:
#                 problem_closePosition_list.append(new_positions_data['symbol'])

#         # if success_closePosition_list and problem_closePosition_list:
#         # cancel_orders_list, unSuccess_cancel_orders_list = await self.cancel_all_orders_for_position(success_closePosition_list)  
#         cancel_orders_list, unSuccess_cancel_orders_list = await self.cancel_order_by_id(success_closePosition_list)
#         # elif success_closePosition_list and not problem_closePosition_list:
#         # cancel_orders_list, unSuccess_cancel_orders_list = await self.cancel_all_open_orders()              

#         return success_closePosition_list, problem_closePosition_list, cancel_orders_list, unSuccess_cancel_orders_list
 
    
    
#     # /////////////////////////////////////////////////////////////////////////////////////////////////////




# # self.MIN_VOLUM_DOLLARS

# # utils_apii = UTILS_API() 

# # # python -m API.orders_utils
    











# #         def try_to_close_by_market_open_position_by_stake(self, main_stake):

# #         close_pos_by_market = None            
# #         is_selling = -1
# #         target_price = None
# #         market_type = 'MARKET'
# #         succes_closed_symbol_list = []
# #         dont_closed_symbol_list = []

# #         for item in main_stake:
# #             success_flag = False
# #             try:
# #                 _, success_flag = self.make_order(item, is_selling, target_price, market_type)
                
# #                 if success_flag:
# #                     succes_closed_symbol_list.append(item["symbol"])
# #                 else:
# #                     dont_closed_symbol_list.append(item["symbol"])
                    
# #             except Exception as ex:
# #                 # print(ex)
# #                 dont_closed_symbol_list.append(item["symbol"])
# #                 continue

# #         return succes_closed_symbol_list, dont_closed_symbol_list
    
# #     def try_to_close_by_market_all_open_positions(self, main_stake):

# #         all_positions = None   
# #         succes_closed_symbol_list = []     
# #         dont_closed_symbol_list = []    
# #         is_selling = -1
# #         target_price = None
# #         market_type = 'MARKET'
# #         all_openPos_symbols = []

# #         try:
# #             all_positions = self.get_open_positions()  
# #         except Exception as ex:
# #             print(ex)

# #         all_openPos_symbols = [x["symbol"] for x in all_positions]  
# #         # print(all_openPos_symbols)     

# #         for item in main_stake:
# #             success_flag = False 
# #             # print(item)
# #             if item["symbol"] in all_openPos_symbols:
# #                 try:
# #                     _, success_flag = self.make_order(item, is_selling, target_price, market_type)
# #                     if success_flag:
# #                         succes_closed_symbol_list.append(item["symbol"])
# #                     else:
# #                         dont_closed_symbol_list.append(item["symbol"])                
# #                 except Exception as ex:
# #                     # print(ex)
# #                     dont_closed_symbol_list.append(item["symbol"])
# #                     # close_pos_by_market_answer_list.append(ex)
# #                     continue

# #         return succes_closed_symbol_list, dont_closed_symbol_list


    

    def calc_qnt_func(self, symbol, price, depo, rounding_type='round'): 
        symbol_info = None
        symbol_data = None 
        price_precision = None
        quantity_precision = None
        quantity = None  
        notional = None
        recalc_depo = None
        usdt_flag = False
        # min_qnt = None 
        if depo.endswith('USDT'):
            depo = float(depo.replace('USDT', '').strip())
            print(depo*2)
            usdt_flag = True
        elif depo.endswith(f"{symbol.replace('USDT', '').strip()}"):            
            depo = depo.upper()
            depo = float(depo.replace(f"{symbol.replace('USDT', '').strip()}", '').strip())
            print(depo*2)

        # return
        
        try:
            symbol_info = self.get_excangeInfo(symbol)
        except Exception as ex:
            logging.exception(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")  

        if symbol_info:
            try:
                symbol_data = next((item for item in symbol_info["symbols"] if item['symbol'] == symbol), None)
                # print(symbol_data)
            except Exception as ex:
                logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")  
            
        if symbol_data:
        
            try:
                tick_size = float(symbol_data['filters'][0]["tickSize"])
                lot_size_filter = next((f for f in symbol_data.get('filters', []) if f.get('filterType') == 'LOT_SIZE'), None)
                if lot_size_filter:
                    quantity_precision = -int(math.log10(float(lot_size_filter.get('stepSize', '1'))))
                    print(f"quantity_precision: {quantity_precision}")
                
                min_qnt = float(next((f['minQty'] for f in symbol_data['filters'] if f['filterType'] == 'LOT_SIZE'), None))
                max_qnt = float(next((f['maxQty'] for f in symbol_data['filters'] if f['filterType'] == 'LOT_SIZE'), None))

                minNotional = float(next((f['minNotional'] for f in symbol_data['filters'] if f['filterType'] == 'NOTIONAL'), None))
                maxNotional = float(next((f['maxNotional'] for f in symbol_data['filters'] if f['filterType'] == 'NOTIONAL'), None))

            except Exception as ex:
                logging.error(f"An error occurred: {ex}")

            try:
                price_precision = self.count_multipliter_places(tick_size)                    
            except Exception as ex:
                print(ex)
            
            try:
                print(f"notional: {minNotional}") 
                print(f"notional: {maxNotional}")       
               
                if depo <= minNotional:
                    depo = minNotional               
                elif depo >= maxNotional:
                    depo = maxNotional 
                if rounding_type == 'round':
                    quantity = round(depo / price, quantity_precision)
                                    
            except Exception as ex:
                logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 

        return quantity, recalc_depo, price_precision

# //////////////////////////////////////////////////////////////////////////////

    def json_write_trades(self, formatted_trades, symbol):
        
        output_file=f'{symbol}_tradesBook.json'
        with open(output_file, 'w') as json_file:
            json.dump(formatted_trades, json_file, indent=2)

    def csv_write_trades(self, data, symbol, cur_time):
        output_file = f'{symbol}_{cur_time}_tradesBook.csv'
        
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Ticker', 'Date', 'Amount', 'Amount_Usdt', 'Commission', 'Side', 'Price', 'Profit', 'Total_Profit', 'Total_Average_Buy_Price', 'Total_Amount'])

            for trade in data:
                ticker = trade['Ticker']
                date = trade['Date']                
                amount = trade['Amount']
                usdt_amount = trade['Amount_Usdt']
                commission = trade['Commission']
                side = trade['Side']
                price = trade['Price']

                profit = trade['Profit']
                total_profit = trade['Total_Profit']
                total_Average_BuyPrice = trade['Total_Average_Buy_Price']
                total_balance = trade['Total_Amount']
                
                writer.writerow([ticker, date, amount, usdt_amount, commission, side, price, profit, total_profit, total_Average_BuyPrice, total_balance])

    def calculate_profit_and_amount_flow_json(self, data):
        
        sorted_data = sorted(data, key=lambda x: x['timestamp'])

        formatted_trades = []
        total_buy_amount_for_result = 0
        total_buy_cost_for_result = 0
        total_buy_amount_for_calc = 0
        total_buy_cost_for_calc = 0        
        total_profit = 0
        amount_flow = 0
        amount = 0
        total_buy_price_flow = ''
        prev_side = None        
        average_buy_price_for_result = 0
        average_buy_price_for_result_for_blanc = ''

        for i, trade in enumerate(sorted_data):
        
            profit = 0
            ticker = trade['symbol'].replace('/','')
            timestamp_ms = trade['timestamp']
            date = datetime.utcfromtimestamp(timestamp_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')
            amount = trade['amount']
            usdt_amount = trade['cost']
            side = 'Buy' if trade['side'] == 'buy' else 'Sell'
            try:                    
                prev_side = 'Buy' if sorted_data[-1]['side'] == 'buy' else 'Sell'
            except:
                prev_side = None
            price = trade['price']
            commission = trade['fee']['cost']

            if side == 'Buy':
                if prev_side and prev_side == 'Sell':                                               
                    total_buy_amount_for_calc = 0
                    total_buy_cost_for_calc = 0
                    average_buy_price_for_calc = 0              

                total_buy_amount_for_calc += amount
                total_buy_cost_for_calc += usdt_amount
                total_buy_amount_for_result += amount
                total_buy_cost_for_result += usdt_amount
                average_buy_price_for_result = total_buy_cost_for_result / total_buy_amount_for_result
                # print(average_buy_price_for_result)

                amount_flow += amount
                

            elif side == 'Sell':
                amount_flow -= amount
                if amount_flow < 0:
                    amount_flow += amount
                    continue 
                else:
                    average_buy_price_for_calc = total_buy_cost_for_calc / total_buy_amount_for_calc
                    profit = (amount * price) - commission - (amount * average_buy_price_for_calc )                   

            if profit !=0:
                total_profit += profit
            else:
                profit = ''

            if i == len(sorted_data) - 1:
                # print('fmvh bk kfv jn')
                total_buy_price_flow = amount_flow 
                total_total_profit = total_profit
                average_buy_price_for_result_for_blanc = average_buy_price_for_result
                                
            else:
                total_buy_price_flow = ''
                total_total_profit = ''
                average_buy_price_for_result_for_blanc = ''            
        
            formatted_trade = {
                'Ticker': ticker,
                'Date': date,
                'Amount': amount,
                'Amount_Usdt': usdt_amount,
                'Commission': commission,
                'Side': side,
                'Price': price,
                'Profit': profit,
                'Total_Profit': total_total_profit,
                'Total_Average_Buy_Price': average_buy_price_for_result_for_blanc,
                'Total_Amount': total_buy_price_flow
            }
            formatted_trades.append(formatted_trade)
         


        return formatted_trades

    def get_myBook(self, symbol):
        formatted_trades = None
        trades_symbol_list = []
        try:
            # trades_symbol_list = self.exchange.fetch_total_balance()
            # trades_symbol_list = [key for key, value in trades_symbol_list.items() if float(value) !=0 and key != 'USDT']
            # print(trades_symbol_list)
            trades_data = self.exchange.fetch_my_trades(symbol)
            formatted_trades = self.calculate_profit_and_amount_flow_json(trades_data)
            # print(f"len(formatted_trades): {len(formatted_trades)}")
            if formatted_trades:
                # self.json_write_trades(formatted_trades, symbol)
                cur_time = str(datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')).replace('-','_').replace(':','_').replace(' ','__')
                self.csv_write_trades(formatted_trades, symbol, cur_time)
            
            return True
        except Exception as ex:
            logging.exception(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

        return False

# utils_apii = UTILS_APII()
# symbol = 'BTCUSDT'
# print(utils_apii.get_myBook(symbol))

# python -m API_BINANCE.utils_api
    

# # spot:
# {'symbol': 'BTCUSDT', 'status': 'TRADING', 'baseAsset': 'BTC', 'baseAssetPrecision': 8, 'quoteAsset': 'USDT', 'quotePrecision': 8, 'quoteAssetPrecision': 8, 'baseCommissionPrecision': 8, 'quoteCommissionPrecision': 8, 'orderTypes': ['LIMIT', 'LIMIT_MAKER', 'MARKET', 'STOP_LOSS_LIMIT', 'TAKE_PROFIT_LIMIT'], 'icebergAllowed': True, 'ocoAllowed': True, 'quoteOrderQtyMarketAllowed': True, 'allowTrailingStop': True, 'cancelReplaceAllowed': True, 'isSpotTradingAllowed': True, 'isMarginTradingAllowed': True, 'filters': [{'filterType': 'PRICE_FILTER', 'minPrice': '0.01000000', 'maxPrice': '1000000.00000000', 'tickSize': '0.01000000'}, {'filterType': 'LOT_SIZE', 'minQty': '0.00001000', 'maxQty': '9000.00000000', 'stepSize': '0.00001000'}, {'filterType': 'ICEBERG_PARTS', 'limit': 10}, {'filterType': 'MARKET_LOT_SIZE', 'minQty': '0.00000000', 'maxQty': '147.10456291', 'stepSize': '0.00000000'}, {'filterType': 'TRAILING_DELTA', 'minTrailingAboveDelta': 10, 'maxTrailingAboveDelta': 2000, 'minTrailingBelowDelta': 10, 'maxTrailingBelowDelta': 2000}, {'filterType': 'PERCENT_PRICE_BY_SIDE', 'bidMultiplierUp': '5', 'bidMultiplierDown': '0.2', 'askMultiplierUp': '5', 'askMultiplierDown': '0.2', 'avgPriceMins': 5}, {'filterType': 'NOTIONAL', 'minNotional': '5.00000000', 'applyMinToMarket': True, 'maxNotional': '9000000.00000000', 'applyMaxToMarket': False, 'avgPriceMins': 5}, {'filterType': 'MAX_NUM_ORDERS', 'maxNumOrders': 200}, {'filterType': 'MAX_NUM_ALGO_ORDERS', 'maxNumAlgoOrders': 5}], 'permissions': ['SPOT', 'MARGIN', 'TRD_GRP_004', 'TRD_GRP_005', 'TRD_GRP_006', 'TRD_GRP_009', 'TRD_GRP_010', 'TRD_GRP_011', 'TRD_GRP_012', 'TRD_GRP_013', 'TRD_GRP_014', 'TRD_GRP_015', 'TRD_GRP_016', 'TRD_GRP_017', 'TRD_GRP_018', 'TRD_GRP_019', 'TRD_GRP_020', 'TRD_GRP_021', 'TRD_GRP_022', 'TRD_GRP_023', 'TRD_GRP_024', 'TRD_GRP_025'], 'defaultSelfTradePreventionMode': 'EXPIRE_MAKER', 'allowedSelfTradePreventionModes': ['EXPIRE_TAKER', 'EXPIRE_MAKER', 'EXPIRE_BOTH']}

# {'symbol': 'BTCUSDT', 'orderId': 24421604067, 'orderListId': -1, 'clientOrderId': 'PkEqgPCNW2DlkL5vvsSmM1', 'transactTime': 1705772569051, 'price': '0.00000000', 'origQty': '0.00029000', 'executedQty': '0.00029000', 'cummulativeQuoteQty': '12.04976970', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'BUY', 'workingTime': 1705772569051, 'fills': [{'price': '41550.93000000', 'qty': '0.00029000', 'commission': '0.00000029', 'commissionAsset': 'BTC', 'tradeId': 3381894408}], 'selfTradePreventionMode': 'EXPIRE_MAKER'}


    # Общая цена покупки = Σ(цена акции * количество акций)
    # Общее количество = Σ(количество акций)
    # Средняя цена = общая покупка цена / общее количество