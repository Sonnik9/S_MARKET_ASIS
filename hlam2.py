


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


            
            # if self.tp_mode == 'A':
            #     timeframe = '15m'
            #     limit = 100
            #     m1_15_data = self.get_ccxtBinance_klines(symbol, timeframe, limit)            
            #     m1_15_data['TR'] = abs(m1_15_data['High'] - m1_15_data['Low'])
            #     m1_15_data['ATR'] = m1_15_data['TR'].rolling(window=14).mean()
            #     item['atr'] = m1_15_data['ATR'].iloc[-1]


    # def get_price_precession(self, symbol):
    #     price_precision = None
    #     symbol_info = None
    #     symbol_data = None
    #     tick_size = None
    #     try:
    #         symbol_info = self.get_excangeInfo(symbol)
    #         if symbol_info:   
    #             symbol_data = next((item for item in symbol_info["symbols"] if item['symbol'] == symbol), None)
    #             # print(symbol_data)
    #         if symbol_data:       
    #             tick_size = float(symbol_data['filters'][0]["tickSize"])
    #             price_precision = self.count_multipliter_places(tick_size)      
    #     except Exception as ex:
    #         logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")  

    #     return price_precision


    # def json_write_trades(self, formatted_trades, symbol):
        
    #     output_file=f'{symbol}_tradesBook.json'
    #     with open(output_file, 'w') as json_file:
    #         json.dump(formatted_trades, json_file, indent=2)

            # /////////////////////////////////////////////////////////////////////////////// 
                
            # @self.bot.message_handler(func=lambda message: message.text not in self.reserved_frathes_list)
            # def handle_exceptionsInput(message):
            #     try:
            #         response_message = f"Try again and enter a valid option."
            #         message.text = self.connector_func(message, response_message)   
            #     except Exception as ex:
            #         logging.exception(
            #             f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")  
            
            


#     def req(self, url, headers, n):
        
#         data_tickers = []
#         coin_name = None
#         week_dinamic = None
#         day_dinamic = None
#         oneHour_dinamic = None
#         position_ind = None
#         r = requests.get(url, headers=headers)
#         print(r)
#         soup = BeautifulSoup(r.text, 'lxml')
#         tablee = soup.find('div', class_='position-relative').find('table')
#         parent_trs = tablee.find_all('tr', recursive=True)

#         for i, tik in enumerate(parent_trs):
#             position_ind = (n-1)*100 + i
#             coin_name = None
#             coin_name_pre = None
#             week_dinamic = None
#             week_dinamic_pre = None
#             day_dinamic = None
#             day_dinamic_pre = None
#             oneHour_dinamic = None
#             oneHour_dinamic_pre = None
#             try:
#                 coin_name_pre = tik.find('td', class_='coin-name')
#                 if coin_name_pre:
#                     coin_name = coin_name_pre.find_all('span')[1].text.strip()
#             except:
#                 continue
#             try:
#                 week_dinamic_pre = tik.find('td', class_='td-change7d')
#                 if week_dinamic_pre:
#                     week_dinamic = float(week_dinamic_pre.get_text(separator=' ', strip=True).split('%')[0])
#             except:
#                 continue
#             try:
#                 day_dinamic_pre = tik.find('td', class_='td-change24h')
#                 if day_dinamic_pre:
#                     day_dinamic = float(day_dinamic_pre.get_text(separator=' ', strip=True).split('%')[0])
#             except:
#                 continue
#             try:
#                 oneHour_dinamic_pre = tik.find('td', class_='td-change1h')
#                 if oneHour_dinamic_pre:
#                     oneHour_dinamic = float(oneHour_dinamic_pre.get_text(separator=' ', strip=True).split('%')[0])
#             except:
#                 continue

#             # td_elements = tik.find_all('td')

#             # for td in td_elements:
#             #     classes = td.get_attribute_list('class')       
#             #     if 'coin-name' in classes:              
#             #         coin_name = td.find_all('span')[1].text.strip()
        
#             #     if 'td-change7d' in classes:
#             #         try:
#             #             week_dinamic = float(td.get_text(separator=' ', strip=True).split('%')[0])
#             #         except:
#             #             continue
        
#             #     if 'td-change24h' in classes:
#             #         try:
#             #             day_dinamic = float(td.get_text(separator=' ', strip=True).split('%')[0])
#             #         except:
#             #             continue
#             #     if 'td-change1h' in classes:
#             #         try:
#             #             oneHour_dinamic = float(td.get_text(separator=' ', strip=True).split('%')[0])
#             #         except:
#             #             continue
#             if coin_name and week_dinamic and day_dinamic and oneHour_dinamic:
#                 data_tickers.append((coin_name, week_dinamic, day_dinamic, oneHour_dinamic, position_ind))

#         return data_tickers[1:]

#     def process_parser(self):
#         tickers = None
#         tickers_list = []
#         headers = {
#             'authority': 'pagead2.googlesyndication.com',
#             'accept': '*/*',
#             'accept-language': 'en-US,en;q=0.9',
#             'cache-control': 'max-age=0',
#             'referer': 'https://fd8e368e638676c19e503d549675a66f.safeframe.googlesyndication.com/',
#             'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
#             'sec-ch-ua-mobile': '?0',
#             'sec-ch-ua-platform': '"Linux"',
#             'sec-fetch-dest': 'empty',
#             'sec-fetch-mode': 'no-cors',
#             'sec-fetch-site': 'same-site',
#             'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#             'x-client-data': 'CIm2yQEIo7bJAQipncoBCN3wygEIlKHLAQiHoM0BCMzuzQEIg/DNARiPzs0BGKfqzQEY+vLNAQ==',
#         }
#         # for n in range(1, 2, 1):
#             # url = f'https://www.coingecko.com/en?page={n}'
#         url = f'https://pagead2.googlesyndication.com/pcs/activeview?xai=AKAOjsudPaJgrSrUFVzXRhHGHzao2CV9nYhUDlVlYj7NgIs7b2MQuk-uFh-ZjxU2epTapvQO7L1TvfWewnqHYScnAFRJ7MKZ3auZCmNtWgh1SJw-qxjWXiAmB_XhNFBe7E-ZujKSgXUqUyOZ71eeKHECX6yAzcEOjfo3Bw&sig=Cg0ArKJSzP5UxgWGS6mQEAE&id=lidartos&mcvt=33933&p=164,467,254,1437&mtos=33933,33933,33933,33933,33933&tos=34677,0,0,0,0&v=20240129&bin=7&avms=nio&bs=0,0&mc=1&if=1&app=0&itpl=30&adk=1722924575&rs=4&la=0&cr=0&uach=WyJMaW51eCIsIjYuMC4wIiwieDg2IiwiIiwiMTIwLjAuNjA5OS4yMTYiLG51bGwsMCxudWxsLCI2NCIsW1siTm90X0EgQnJhbmQiLCI4LjAuMC4wIl0sWyJDaHJvbWl1bSIsIjEyMC4wLjYwOTkuMjE2Il0sWyJHb29nbGUgQ2hyb21lIiwiMTIwLjAuNjA5OS4yMTYiXV0sMF0%3D&vs=4&r=b&co=170663554101&rst=1706635541160&rpt=1493&isd=0&lsd=0&ec=1&met=ie&wmsd=0&pbe=0&vae=0&spb=0&ffslot=0&reach=0&io2=0'
#         tickers = self.req(url, headers)

#         if tickers:
#             tickers_list += tickers

#         # print(len(tickers_list))
#         ranging_coins_list = sorted(tickers_list, key=lambda x: x[1], reverse=True)
#         # final_coins_list = list(filter(lambda item: item[1] > 5, ranging_coins_list))
#         file_name = f'coins_for_prep_{len(ranging_coins_list)}'
#         # now = datetime.now() 
#         # curentTimeForFile = now.strftime("%d_%m_%Y__%H_%M")
#         # w_r_flag = 'w'
#         # txt_redactor.txt_redactor_func(final_coins_list, curentTimeForFile, w_r_flag, file_name)  

#         return ranging_coins_list

