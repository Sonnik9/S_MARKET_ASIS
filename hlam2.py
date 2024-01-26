


        # return tp_tg_response
        
        # return item
            
# {'info': {'symbol': 'BTCUSDT', 'id': '3381919667', 'orderId': '24421877188', 'orderListId': '-1', 'price': '41608.00000000', 'qty': '0.00029000', 'quoteQty': '12.06632000', 'commission': '0.00000029', 'commissionAsset': 'BTC', 'time': '1705775204887', 'isBuyer': True, 'isMaker': False, 'isBestMatch': True}, 'timestamp': 1705775204887, 'datetime': '2024-01-20T18:26:44.887Z', 'symbol': 'BTC/USDT', 'id': '3381919667', 'order': '24421877188', 'type': None, 'side': 'buy', 'takerOrMaker': 'taker', 'price': 41608.0, 'amount': 0.00029, 'cost': 12.06632, 'fee': {'cost': 2.9e-07, 'currency': 'BTC'}, 'fees': [{'cost': 2.9e-07, 'currency': 'BTC'}]}
# None
# None
    
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

