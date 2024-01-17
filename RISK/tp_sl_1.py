import logging, os, inspect

logging.basicConfig(filename='TEMPLATES/config_log.log', level=logging.ERROR)
current_file = os.path.basename(__file__)

class RISK_MANAGEMENT():

    def __init__(self) -> None:
        pass

    async def static_tp_calc(self, item, static_TP_flag, atr_TP_flag, tp_ratio, atr_TP_coef):
        
        tp_price = None
        enter_deFacto_price, atr, price_precision, tick_size = item['enter_deFacto_price'], item['atr'], item['price_precision'], item['tick_size']
        
        try:
            if static_TP_flag:                      
                tp_price = item['tp_price'] = round(enter_deFacto_price * (1 + (tp_ratio/100)), tick_size)
            elif atr_TP_flag:       
                # print(f"price_precision == tick_size: {price_precision == tick_size}")                   
                tp_price = item['tp_price'] = round(enter_deFacto_price + (atr * atr_TP_coef), tick_size)                
        except Exception as ex:
            logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 

        return tp_price

