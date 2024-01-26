from API_BINANCE.get_api import GETT_API
import time
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
            # print(url)
            params = {}        
            params["symbol"] = item["symbol"]   
            # print(params["symbol"])  
            params["type"] = market_type
            # print(params["type"])  
            params["quantity"] = item['qnt']      
        
            if market_type == 'LIMIT':            
                params["price"] = target_price
                params["timeInForce"] = 'GTC' 
                # params['recvWindow'] = 5000
    
            if is_selling == 1:
                side = 'BUY'
            elif is_selling == -1:
                side = "SELL" 
            params["side"] = side 

            params = self.get_signature(params)
            print(params)
            response = self.HTTP_request(url, method=method, headers=self.header, params=params)
            print(response)
            if response and 'clientOrderId' in response and response['side'] == side:
                success_flag = True
        except Exception as ex:
            logging.exception(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

        return response, success_flag


# {'symbol': 'BTCUSDT', 'type': 'LIMIT', 'quantity': 0.00029, 'price': 43272.32, 'timeInForce': 'GTC', 'side': 'SELL', 'timestamp': 1706299801833, 'signature': 'c5b4db2f61e728b8f6a5f663134b614c9fcf15d54ed738e2f5a46a3885cd0b71'}
# {'symbol': 'BTCUSDT', 'orderId': 24541484934, 'orderListId': -1, 'clientOrderId': 'ECPk0Tbnme3077Z7QsmPBP', 'transactTime': 1706299802529, 'price': '43272.32000000', 'origQty': '0.00029000', 'executedQty': '0.00000000', 'cummulativeQuoteQty': '0.00000000', 'status': 'NEW', 'timeInForce': 'GTC', 'type': 'LIMIT', 'side': 'SELL', 'workingTime': 1706299802529, 'fills': [], 'selfTradePreventionMode': 'EXPIRE_MAKER'}
