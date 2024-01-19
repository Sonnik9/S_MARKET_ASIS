from API_BINANCE.delete_api import DELETEE_API 
from RISK.tp_sl_1 import RISK_MANAGEMENT
from datetime import datetime
from decimal import Decimal, ROUND_DOWN
import math
import asyncio
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
    
    def calc_qnt_func(self, symbol, price, depo): 
        symbol_info = None
        symbol_data = None 
        price_precision = None
        quantity_precision = None
        quantity = None  
        notional = None
        recalc_depo = None
        # min_qnt = None 
        if depo.endswith('USDT'):
            depo = float(depo.replace('USDT', '').strip())
            print(depo*2)
        if depo.endswith(f"{symbol.replace('USDT', '').strip()}"):            
            depo = depo.upper()
            depo = float(depo.replace(f"{symbol.replace('USDT', '').strip()}", '').strip())
            print(depo*2)

        return
        
        # try:
        #     symbol_info = self.get_excangeInfo(symbol)
        # except Exception as ex:
        #     logging.exception(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")  

        # if symbol_info:
        #     try:
        #         symbol_data = next((item for item in symbol_info["symbols"] if item['symbol'] == symbol), None)
        #     except Exception as ex:
        #         logging.exception(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
            
        # if symbol_data:   
        #     print(symbol_data)         
        #     try:                
        #         tick_size = float(symbol_data['filters'][0]["tickSize"])
        #         price_precision = int(symbol_data['pricePrecision']) 
        #         # print(f"price_precision: {price_precision}")           
        #         quantity_precision = int(symbol_data['quantityPrecision']) 
        #         lot_size_filter = next((item for item in symbol_data['filters'] if item['filterType'] == 'MIN_NOTIONAL'), None)  
        #         notional = float(lot_size_filter.get('notional', None))
        #         print(f"notional: {notional}")
                
        #     except Exception as ex:
        #         logging.exception(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
        
        #     try:
        #         tick_size = self.count_multipliter_places(tick_size)
        #         print(f"tick_size: {tick_size}")
        #     except Exception as ex:
        #         logging.exception(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 
            
        #     try:  
        #         if depo <= notional:
        #             depo = notional  
        #         quantity = round(depo / price, quantity_precision)
        #         # quantity = round(depo / price, tick_size)
        #         recalc_depo = quantity * price     
        #         print(f"quantity: {quantity}")
        #         # print(f"{symbol}:  {quantity, recalc_depo, price_precision, tick_size}")
        #     except Exception as ex:
        #         logging.exception(f"An error occurred: {ex}")

        # return quantity, recalc_depo, price_precision, tick_size
    
    
# ///////////////////////////////////////////////////////////////////////////////////
    def buy_market_order_temp_func(self, item, depo):
        itemm = item.copy()        
        symbol = itemm["symbol"]        
        atr = itemm["atr"]
        entry_price = itemm["current_price"]
        enter_deJure_price = itemm["current_price"]

        try:                    
            itemm['qnt'], itemm["recalc_depo"], itemm["price_precision"], itemm["tick_size"] = self.calc_qnt_func(symbol, enter_deJure_price, depo)            
        except Exception as ex:
            logging.exception(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
        print(f"{symbol}:\nitemm['qnt'] before: {itemm['qnt']}") 
        if itemm['qnt']:
            is_selling = 1
            success_flag = False
            market_type = 'MARKET'
            target_price = None
            try:          
                open_market_order, success_flag = self.make_order(itemm, is_selling, target_price, market_type)
                print(f"open_market_order:  {open_market_order}") 
            except Exception as ex:
                logging.exception(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
            if success_flag:                
                try:
                    itemm["enter_deFacto_price"] = self.get_DeFacto_price(symbol)
                    print(f'str73 {symbol}:  {itemm["enter_deFacto_price"]}  (defacto_prtice)')
                    itemm["done_level"] = 1                                        
                except Exception as ex:
                    logging.exception(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}\n{open_market_order}")

        return itemm

#     async def tp_make_orders(self, item):
#         itemm = item.copy()
#         is_selling = -1
#         tp_price = None 
#         sl_price = None

#         try:           
#             success_flag = False   
#             tp_ratio = self.TP_rate
#             sl_ratio = self.SL_ratio
#             tp_price, sl_price = await self.static_tp_calc(itemm, tp_ratio, sl_ratio)
            
#             print(f"target_TPprice before transformed: {tp_price}")
#             # try:
#             #     target_price = self.transformed_price(itemm["symbol"], target_price)
#             #     print(f"target_price transformed: {target_price}")
#             # except Exception as pe:
#             #     print(pe)
#             #     logging.warning(f"Precision error in transforming price: {pe}")

            
#             print(f"target_price: {tp_price}")
#             market_type = 'TAKE_PROFIT_MARKET' 
            
#             open_static_tp_order, success_flag = await self.make_order(itemm, is_selling, tp_price, market_type)
#             print(f'open_static_tp_order  {open_static_tp_order}')

#             if self.stopLoss_flag:
#                 if success_flag:                           
#                     success_flag = False               
#                     market_type = 'STOP_MARKET'                                 
#                     open_static_sl_order, success_flag = await self.make_order(itemm, is_selling, sl_price, market_type)
#                     print(f'open_static_sl_order  {open_static_sl_order}')
#                     if success_flag:                                     
#                         itemm["done_level"] = 2   

#             else:
#                 if success_flag:                                     
#                     itemm["done_level"] = 2 

        
#         except Exception as ex:
#             logging.exception(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}\n{open_static_tp_order}")

#         return itemm 
    
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

# # # ///////////////////////////////////////////////////////////////////////////////////////
    

# # symbol_data = {'symbol': 'ETHUSDT', 'pair': 'ETHUSDT', 'contractType': 'PERPETUAL', 'deliveryDate': 4133404800000, 'onboardDate': 1569398400000, 'status': 'TRADING', 'maintMarginPercent': '2.5000', 'requiredMarginPercent': '5.0000', 'baseAsset': 'ETH', 'quoteAsset': 'USDT', 'marginAsset': 'USDT', 'pricePrecision': 2, 'quantityPrecision': 3, 'baseAssetPrecision': 8, 'quotePrecision': 8, 'underlyingType': 'COIN', 'underlyingSubType': [], 'settlePlan': 0, 'triggerProtect': '0.0500', 'liquidationFee': '0.020000', 'marketTakeBound': '0.10', 'maxMoveOrderLimit': 10000, 'filters': [{'maxPrice': '95264.25', 'filterType': 'PRICE_FILTER', 'tickSize': '0.01', 'minPrice': '18.67'}, {'minQty': '0.001', 'stepSize': '0.001', 'maxQty': '10000', 'filterType': 'LOT_SIZE'}, {'filterType': 'MARKET_LOT_SIZE', 'stepSize': '0.001', 'minQty': '0.001', 'maxQty': '10000'}, {'filterType': 'MAX_NUM_ORDERS', 'limit': 200}, {'filterType': 'MAX_NUM_ALGO_ORDERS', 'limit': 10}, {'filterType': 'MIN_NOTIONAL', 'notional': '20'}, {'multiplierDown': '0.9000', 'filterType': 'PERCENT_PRICE', 'multiplierDecimal': '4', 'multiplierUp': '1.1000'}], 'orderTypes': ['LIMIT', 'MARKET', 'STOP', 'STOP_MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET', 'TRAILING_STOP_MARKET'], 'timeInForce': ['GTC', 'IOC', 'FOK', 'GTX', 'GTD']}
# # lot_size_filter = next((item for item in symbol_data['filters'] if item['filterType'] == 'LOT_SIZE'), None)  
# # notional = float(lot_size_filter['notional'])
# # print(notional)