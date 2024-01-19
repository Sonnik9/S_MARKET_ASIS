from API_BINANCE.get_api import GETT_API


class POSTT_API(GETT_API):

    def __init__(self) -> None:        
        super().__init__() 

class POSTT_API(GETT_API):

    def __init__(self) -> None:        
        super().__init__()  
    
    def make_stop_limit_order(self, item, is_closing, stop_price, limit_price, quantity):
        method = 'POST'
        
        response = None
        success_flag = False
        url = self.URL_PATTERN_DICT['create_order_url']
        params = {}        
        params["symbol"] = item["symbol"]
        params["quantity"] = quantity

        if is_closing == 1:
            side = 'SELL'
        elif is_closing == -1:
            side = 'BUY'
        params["side"] = side 

        params["type"] = 'LIMIT'
        params["timeInForce"] = 'GTC' 
        params["price"] = limit_price

        # Добавляем параметры для стоп-лимит ордера
        params["stopPrice"] = stop_price
        params["newOrderRespType"] = 'FULL'  # Вернуть полную информацию об ордере

        params = self.get_signature(params)
        response = self.HTTP_request(url, method=method, headers=self.header, params=params)
        print(response)
        
        if response and 'status' in response and response['status'] == 'NEW':
            success_flag = True

        return response, success_flag
 
    
    def make_order(self, item, is_closing, target_price, market_type):
        method = 'POST'
        
        response = None
        success_flag = False
        url = self.URL_PATTERN_DICT['create_order_url']
        params = {}        
        params["symbol"] = item["symbol"]        
        params["type"] = market_type
        params["quantity"] = item['qnt']
      
        if market_type == 'LIMIT':            
            params["price"] = target_price
            params["timeinForce"] = 'GTC' 
            
        if market_type == 'STOP_MARKET' or market_type == 'TAKE_PROFIT_MARKET':
            params['stopPrice'] = target_price
            params['closePosition'] = True 
  
        if is_closing == 1:
            side = 'BUY'
        elif is_closing == -1:
            side = "SELL" 
        params["side"] = side 

        params = self.get_signature(params)
        response = self.HTTP_request(url, method=method, headers=self.header, params=params)
        print(response)
        if response and 'status' in response and response['status'] == 'NEW':
            success_flag = True

        return response, success_flag
    
# post_apii = POSTT_API()
# # symbol = 'MATICUSDT'
# symbol = 'SOLUSDT'
# rec = post_apii.set_margin_type(symbol)
# print(rec)
# rec = post_apii.set_leverage(symbol, 4)
# print(rec)

