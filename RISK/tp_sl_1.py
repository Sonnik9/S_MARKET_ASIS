import logging, os, inspect

logging.basicConfig(filename='TEMPLATES/config_log.log', level=logging.ERROR)
current_file = os.path.basename(__file__)

class RISK_MANAGEMENT():

    def __init__(self) -> None:
        pass

    def static_tp_calc(self, item, static_TP_flag, atr_TP_flag, tp_ratio, atr_TP_coef):
        
        tp_price = None
        current_price, atr, price_precision = item['current_price'], item['atr'], item['price_precision']
                
        try:
            if static_TP_flag:                      
                tp_price = item['tp_price'] = round(current_price * (1 + (tp_ratio/100)), price_precision)
            elif atr_TP_flag:                                  
                tp_price = item['tp_price'] = round(current_price + (atr * atr_TP_coef), price_precision)                
        except Exception as ex:
            logging.error(f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")    

        return tp_price

