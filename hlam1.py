    
    # def make_stop_limit_order(self, item, is_selling, stop_price, limit_price, quantity):
    #     method = 'POST'
        
    #     response = None
    #     success_flag = False
    #     url = self.URL_PATTERN_DICT['create_order_url']
    #     params = {}        
    #     params["symbol"] = item["symbol"]
    #     params["quantity"] = quantity

    #     if is_selling == 1:
    #         side = 'BUY'
    #     elif is_selling == -1:
    #         side = 'SELL'

    #     params["side"] = side
    #     params["type"] = 'LIMIT'
    #     params["timeInForce"] = 'GTC' 
    #     params["price"] = limit_price

    #     # Добавляем параметры для стоп-лимит ордера
    #     params["stopPrice"] = stop_price
    #     params["newOrderRespType"] = 'FULL'  # Вернуть полную информацию об ордере

    #     params = self.get_signature(params)
    #     response = self.HTTP_request(url, method=method, headers=self.header, params=params)
    #     print(response)
        
    #     if response and 'status' in response and response['status'] == 'NEW':
    #         success_flag = True

    #     return response, success_flag

    # def get_balance(self):
       
    #     current_balance = None 
    #     url = self.URL_PATTERN_DICT['balance_url']        
    #     params = {}
    #     params['recvWindow'] = 5000
    #     params = self.get_signature(params)
    #     current_balance = self.HTTP_request(url, method=method, headers=self.header, params=params)
              
    #     current_balance = dict(current_balance)                
    #     current_balanceE = current_balance['balances']
    #     current_balance = [(x['free'], x['locked']) for x in current_balanceE if x['asset'] == 'USDT'][0]

    #     return current_balance



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