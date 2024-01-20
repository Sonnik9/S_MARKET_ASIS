from API_BINANCE.get_api import GETT_API
import logging, os, inspect

logging.basicConfig(filename='config_log.log', level=logging.INFO)
current_file = os.path.basename(__file__)

class POSTT_API(GETT_API):

    def __init__(self) -> None:        
        super().__init__()  
   
    def make_order(self, item, is_selling, target_price, market_type):
        method = 'POST'
        
        response = None
        success_flag = False
        try:
            url = self.URL_PATTERN_DICT['create_order_url']
            params = {}        
            params["symbol"] = item["symbol"]     
            params["type"] = market_type
            params["quantity"] = item['qnt']
        
            if market_type == 'LIMIT':            
                params["price"] = target_price
                params["timeinForce"] = 'GTC' 
    
            if is_selling == 1:
                side = 'BUY'
            elif is_selling == -1:
                side = "SELL" 
            params["side"] = side 

            params = self.get_signature(params)
            response = self.HTTP_request(url, method=method, headers=self.header, params=params)
            print(response)
            if response and 'clientOrderId' in response and response['side'] == side:
                success_flag = True
        except Exception as ex:
            logging.exception(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

        return response, success_flag

