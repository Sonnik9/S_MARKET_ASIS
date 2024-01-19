    
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