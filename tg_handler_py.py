# from tg_assistent_py import TG_ASSISTENT
# import asyncio 
# import time
# import logging, os, inspect

# logging.basicConfig(filename='config_log.log', level=logging.INFO)
# current_file = os.path.basename(__file__)

# money_emoji = "💰"
# rocket_emoji = "🚀"
# lightning_emoji =  "⚡"
# clock_emoji = "⌚"
# film_emoji = "📼"
# percent_emoji = "📶"
# repeat_emoji = "🔁"
# upper_trigon_emoji = "🔼"
# lower_trigon_emoji = "🔽"
# confirm_emoji = "✅"
# link_emoji = "🔗"

# class TG_BUTTON_HANDLER(TG_ASSISTENT):
#     def __init__(self):
#         super().__init__()

#     def open_order_tgButton_handler(self):
#         item = {}  
#         open_order_returned_list = []
#         try:
#             item["symbol"] = self.symbol
#             item['in_position'] = False
#             item['qnt'] = None 
#             item["recalc_depo"] = None 
#             item["price_precision"] = None 
#             item["tick_size"] = None
#             item["current_price"] = self.get_current_price(self.symbol)
#             print(f'item["current_price"]: {item["current_price"]}')

#             timeframe = '15m'
#             limit = 100
#             m1_15_data = self.get_ccxtBinance_klines(self.symbol, timeframe, limit)            
#             m1_15_data['TR'] = abs(m1_15_data['High'] - m1_15_data['Low'])
#             m1_15_data['ATR'] = m1_15_data['TR'].rolling(window=14).mean()
#             item['atr'] = m1_15_data['ATR'].iloc[-1]

#             item = self.make_market_order_temp_func(item)

#             if item['in_position']:
#                 open_order_returned_list.append(1)
#                 item = self.tp_make_orders(item)
#                 if item["done_level"] == 2:
#                     open_order_returned_list.append(2)   
#                 else:
#                     open_order_returned_list.append(-2) 
#             else:
#                 open_order_returned_list.append(-1)
#         except Exception as ex:
#             open_order_returned_list.append(0)
#             print(f"main121: {ex}")

#         return open_order_returned_list
           
#     def go_tgButton_handler(self, message):
#         print('ksdvksfhbvb')
#         cur_time = time.time()
#         tg_response_allow = False
#         last_duration_time = None
#         duration = None
        
#         return_web_socket_task = None
#         return_squeeze_unMomentum_assignator = None
#         return_open_order_tgButton_handler = None
#         answer_open_order_tgButton_handler = None
#         return_info_tgButton_handler = None 
#         answer_tg_reply = None
#         return_closeAll_pos_tgButton_handler = None
#         answer_closeAll_pos_tgButton_handler = None
#         coins_in_squeezeOn = []
#         coins_in_squeezeOff_var = []
#         success_closePosition_list, problem_closePosition_list, cancel_orders_list, unSuccess_cancel_orders_list = [], [], [], []
#         return_closeCustom_pos_tgButton_handler = None
#         answer_closeCustom_pos_tgButton_handler = None

#         tasks = []        

#         while True:
#             # print("Before sleep1")
#             time.sleep(1)
#             # print("After sleep1")
#             try:
#                 # /////////////////////////////////////////////////////////////////////////////////////        
                    
#                 # /////////////////////////////////////////////////////////////////////////////////////


#                 if return_info_tgButton_handler and return_info_tgButton_handler.done():                    
#                     answer_tg_reply = return_info_tgButton_handler.result()
#                     return_info_tgButton_handler = None   
#                     print(answer_tg_reply)
#                     if answer_tg_reply[0]:                        
#                         info_tg_reply = answer_tg_reply[0]     
#                         message.text = self.connector_func(message, info_tg_reply)
#                     elif answer_tg_reply[0] == []:
#                         info_tg_reply = "There is no one open order"
#                         message.text = self.connector_func(message, info_tg_reply)
#                     elif answer_tg_reply[0] == None:
#                         info_tg_reply = "Some problems with getting positions data..."
#                         message.text = self.connector_func(message, info_tg_reply)

#                 # /////////////////////////////////////////////////////////////////////////////////////
                
#                 # /////////////////////////////////////////////////////////////////////////////////////
#                 if self.close_order_triger and self.symbol and self.depo:
#                     self.close_order_triger = False
#                     task5 = [self.close_custom_poss(self.symbol)]
#                     tasks.append(task5)
#                     return_closeCustom_pos_tgButton_handler = asyncio.gather(*task5)

#                 if return_closeCustom_pos_tgButton_handler and return_closeCustom_pos_tgButton_handler.done():
#                     answer_closeCustom_pos_tgButton_handler = return_closeCustom_pos_tgButton_handler.result()
#                     return_closeCustom_pos_tgButton_handler = None
#                     close_tg_reply = ""
#                     success_closePosition_list, problem_closePosition_list, cancel_orders_list, unSuccess_cancel_orders_list = answer_closeCustom_pos_tgButton_handler[0]
#                     close_tg_reply = await self.closePos_template(success_closePosition_list, problem_closePosition_list, cancel_orders_list, unSuccess_cancel_orders_list, close_tg_reply)

#                     success_closePosition_list, problem_closePosition_list, cancel_orders_list, unSuccess_cancel_orders_list = [], [], [], []
#                     message.text = self.connector_func(message, close_tg_reply)
#                 # ///////////////////////////////////////////////////////////////////////////////////////

#                 if self.close_all_orderS_triger:                    
#                     self.close_all_orderS_triger = False
#                     task4 = [self.close_all_poss()]
#                     tasks.append(task4)
#                     return_closeAll_pos_tgButton_handler = asyncio.gather(*task4)

#                 if return_closeAll_pos_tgButton_handler and return_closeAll_pos_tgButton_handler.done():
#                     answer_closeAll_pos_tgButton_handler = return_closeAll_pos_tgButton_handler.result()
#                     return_closeAll_pos_tgButton_handler = None
#                     close_tg_reply = ""
#                     success_closePosition_list, problem_closePosition_list, cancel_orders_list, unSuccess_cancel_orders_list = answer_closeAll_pos_tgButton_handler[0]
#                     close_tg_reply = await self.closePos_template(success_closePosition_list, problem_closePosition_list, cancel_orders_list, unSuccess_cancel_orders_list, close_tg_reply)

#                     success_closePosition_list, problem_closePosition_list, cancel_orders_list, unSuccess_cancel_orders_list = [], [], [], []
#                     message.text = self.connector_func(message, close_tg_reply)
#                 # /////////////////////////////////////////////////////////////////////////////////////

#                 # /////////////////////////////////////////////////////////////////////////////////////
                        
#                 if self.order_triger and self.symbol:
#                     self.order_triger = False
#                     task3 = [self.open_order_tgButton_handler()]
#                     tasks.append(task3)
#                     return_open_order_tgButton_handler = asyncio.gather(*task3)
                    
#                 if return_open_order_tgButton_handler and return_open_order_tgButton_handler.done():
#                     answer_open_order_tgButton_handler = return_open_order_tgButton_handler.result()
#                     if 0 in answer_open_order_tgButton_handler[0]:
#                         order_tg_reply = "Some exceptions with placeing order..." + '\n'
#                         message.text = self.connector_func(message, order_tg_reply)
#                     if -1 in answer_open_order_tgButton_handler[0]:
#                         order_tg_reply = "Some problem with placeing order..." + '\n'
#                         message.text = self.connector_func(message, order_tg_reply)
#                     if -2 in answer_open_order_tgButton_handler[0]:
#                         order_tg_reply = "Some problem with setting takeProfit..." + '\n'
#                         message.text = self.connector_func(message, order_tg_reply)
#                     if 1 in answer_open_order_tgButton_handler[0]:
#                         order_tg_reply = "The order was created successuly!" + '\n'
#                         message.text = self.connector_func(message, order_tg_reply)
#                     if 2 in answer_open_order_tgButton_handler[0]:
#                         order_tg_reply = "The takeProfit was setting successuly!" + '\n'
#                         message.text = self.connector_func(message, order_tg_reply)
#                     return_open_order_tgButton_handler = None


#                 # /////////////////////////////////////////////////////////////////////////////////////

#                 # print("Before sleep2")
#                 await asyncio.sleep(1)
#                 # print("After sleep2")

#             except Exception as ex:
#                 logging.exception(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
