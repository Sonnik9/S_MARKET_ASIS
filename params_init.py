import os
import logging, os, inspect
from dotenv import load_dotenv

logging.basicConfig(filename='API_BINANCE/config_log.log', level=logging.ERROR)
current_file = os.path.basename(__file__)

load_dotenv()

class BASIC_PARAMETRS():
    def __init__(self):        
        self.SOLI_DEO_GLORIA = 'Soli Deo Gloria!'      
        self.market = 'spot'
        self.test_flag = True
        
    def init_api_key(self):
        self.tg_api_token = os.getenv("TG_API_TOKEN", "")
        self.api_key  = os.getenv(f"BINANCE_API_PUBLIC_KEY__TESTNET_{str(self.test_flag)}", "")
        self.api_secret = os.getenv(f"BINANCE_API_PRIVATE_KEY__TESTNET_{str(self.test_flag)}", "")  

        self.header = {
            'X-MBX-APIKEY': self.api_key
        }     

class URL_TEMPLATES(BASIC_PARAMETRS):
    def __init__(self) -> None:
        super().__init__()        
        self.URL_PATTERN_DICT= {}              

    def init_urls(self):  
        if not self.test_flag:       
            self.URL_PATTERN_DICT['current_price_url'] = "https://api.binance.com/api/v3/ticker/price"
            self.URL_PATTERN_DICT['all_tikers_url'] = "https://api.binance.com/api/v3/ticker/24hr"
            self.URL_PATTERN_DICT['create_order_url'] = 'https://api.binance.com/api/v3/order'
            self.URL_PATTERN_DICT['exchange_info_url'] = 'https://api.binance.com/api/v3/exchangeInfo'
            self.URL_PATTERN_DICT['balance_url'] = 'https://api.binance.com/api/v3/account'
            self.URL_PATTERN_DICT['get_all_orders_url'] = 'https://api.binance.com/api/v3/openOrders'
            self.URL_PATTERN_DICT['cancel_all_orders_url'] = 'https://api.binance.com/api/v3/openOrders'
            self.URL_PATTERN_DICT['positions_url'] = 'https://api.binance.com/api/v3/account'
            self.URL_PATTERN_DICT["set_leverage_url"] = 'https://api.binance.com/api/v3/leverage'
            self.URL_PATTERN_DICT["klines_url"] = 'https://api.binance.com/api/v3/klines'
            self.URL_PATTERN_DICT["set_margin_type_url"] = 'https://api.binance.com/api/v3/marginType'

        else:
            self.market = 'futures'
            print('futures test')
            self.URL_PATTERN_DICT['current_ptice_url'] = "https://testnet.binancefuture.com/fapi/v1/ticker/price"
            self.URL_PATTERN_DICT['all_tikers_url'] = "https://testnet.binancefuture.com/fapi/v1/ticker/24hr"
            self.URL_PATTERN_DICT['create_order_url'] = 'https://testnet.binancefuture.com/fapi/v1/order'            
            self.URL_PATTERN_DICT['exchangeInfo_url'] = 'https://testnet.binancefuture.com/fapi/v1/exchangeInfo'
            self.URL_PATTERN_DICT['balance_url'] = 'https://testnet.binancefuture.com/fapi/v2/balance'
            self.URL_PATTERN_DICT['get_all_orders_url'] = 'https://testnet.binancefuture.com/fapi/v1/openOrders'
            self.URL_PATTERN_DICT['cancel_all_orders_url'] = 'https://testnet.binancefuture.com/fapi/v1/allOpenOrders'
            self.URL_PATTERN_DICT['positions_url'] = 'https://testnet.binancefuture.com/fapi/v2/positionRisk'
            self.URL_PATTERN_DICT["set_leverage_url"] = 'https://testnet.binancefuture.com/fapi/v1/leverage'
            self.URL_PATTERN_DICT["klines_url"] = 'https://testnet.binancefuture.com/fapi/v1/klines'
            self.URL_PATTERN_DICT["set_margin_type_url"] = 'https://testnet.binancefuture.com/fapi/v1/marginType'

    
class TIME_TEMPLATES(URL_TEMPLATES):   
    def __init__(self) -> None:
        super().__init__()
        self.KLINE_TIME, self.TIME_FRAME = 15, 'm'
        self.INTERVAL = str(self.KLINE_TIME) + self.TIME_FRAME

class FILTER_SET(TIME_TEMPLATES):
    def __init__(self) -> None:
        super().__init__()
        self.daily_filter_flag = True
        self.SLICE_VOLUME_PAIRS = 50 # volums    
        self.slice_volatilyty_flag = True     
        self.SLICE_VOLATILITY = 40 # volatility
        self.price_filter_flag = False
        self.MIN_FILTER_PRICE = 0.001 # min price
        self.MAX_FILTER_PRICE = 3000000 # max price
        self.problem_pairs = ['USDCUSDT', 'DOGEUSDT'] 
        self.min_volume_usdtFilter_flag = True
        self.MIN_VOLUM_USDT = 100000


class RISKK(FILTER_SET):
    def __init__(self) -> None:
        super().__init__()
        self.static_TP_flag = True        
        self.SL_ratio = 3  # % 
        self.tp_coeff = 1.3
        # /////////////////////////////////////////        
        self.atr_TP_coef = 0.9
        
    def risk_init(self):
        if self.static_TP_flag:
            self.TP_rate = self.SL_ratio *self.tp_coeff  
        else:
            self.atr_TP_flag = True  

class INIT_PARAMS(RISKK):
    def __init__(self) -> None:
        super().__init__()
        self.init_itits()

    def init_itits(self):
        print('helloo')
        self.init_api_key()       
        self.init_urls()        
        self.risk_init()

# params = INIT_PARAMS()
# print(params.test_flag)



# python params_init.py
