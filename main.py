from API_BINANCE.utils_api import UTILS_APII
from datetime import datetime
import time
import logging, os, inspect

logging.basicConfig(filename='config_log.log', level=logging.INFO)
current_file = os.path.basename(__file__)

money_emoji = "💰"
rocket_emoji = "🚀"
lightning_emoji =  "⚡"
clock_emoji = "⌚"
film_emoji = "📼"
percent_emoji = "📶"
repeat_emoji = "🔁"
upper_trigon_emoji = "🔼"
lower_trigon_emoji = "🔽"
confirm_emoji = "✅"
link_emoji = "🔗"

class TG_ASSISTENT(UTILS_APII):

    def __init__(self):
        super().__init__()
        self.seq_control_flag = False 
        self.seq_controlStart_flag = False
        self.dont_seq_control = False
        self.block_acess_flag = False 
        self.block_acess_counter = 0
        self.start_day_date = None

        self.handle_redirect_risk_flag = False

        self.start_flag = False
        self.settings_tg_flag = False
        self.settings_1_redirect_flag = False
        self.settings_2_redirect_flag = False        
        self.open_order_redirect_flag = False
        self.handle_getLink_redirect_flag = False
        self.tp_order_redirect_flag = False
        self.tp_order_auto_redirect_flag = False
        self.tp_order_custom_redirect_flag = False
        self.book_triger_flag = False
        

    def connector_func(self, message, response_message):
        retry_number = 3
        decimal = 1.1       
        for i in range(retry_number):
            try:
                self.bot.send_message(message.chat.id, response_message)                
                return message.text
            except Exception as ex:
                logging.exception(
                    f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

                time.sleep(1.1 + i*decimal)        
                   
        return None

    def date_of_the_month(self):        
        current_time = time.time()        
        datetime_object = datetime.fromtimestamp(current_time)       
        formatted_time = datetime_object.strftime('%d')
        return int(formatted_time)    
  
    def buy_order_tgButton_handler(self, symbol, depo, is_selling):
        item = {}  
        buy_order_returned_list = []
        try:
            # pass
            item["symbol"] = symbol
            item['is_selling'] = is_selling
            item['qnt'] = None 
            item["recalc_depo"] = None 
            item["price_precision"] = None 
            item["tick_size"] = None
            item["atr"] = None
            item["done_level"] = None

            item = self.buy_market_order_temp_func(item, depo, is_selling)

            if item["done_level"] == 1:
                buy_order_returned_list.append(1)
            else:
                buy_order_returned_list.append(-1)

        except Exception as ex:
            logging.exception(
                f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

            buy_order_returned_list.append(0)
            print(f"main121: {ex}")

        return buy_order_returned_list, item['enter_deFacto_price']
    
    def closePos_template(self, success_closePosition_list, problem_closePosition_list, cancel_orders_list, unSuccess_cancel_orders_list, close_tg_reply):
        try:
            print(f"success_closePosition_list, problem_closePosition_list, cancel_orders_list, unSuccess_cancel_orders_list: {success_closePosition_list, problem_closePosition_list, cancel_orders_list, unSuccess_cancel_orders_list}")
            if success_closePosition_list:
                byStr_success_closePosition_list = [str(x) for x in success_closePosition_list]
                close_tg_reply += 'The next positions was closing by succesfully:\n' + ', '.join(byStr_success_closePosition_list) + '\n'
            else:
                close_tg_reply += 'There is no one positions was closing by succesfully' + '\n'
            if problem_closePosition_list:
                byStr_problem_closePosition_list = [str(x) for x in problem_closePosition_list]
                close_tg_reply += 'The next positions was NOT closing by succesfully:\n' + ', '.join(byStr_problem_closePosition_list) + '\n'
            if cancel_orders_list:
                byStr_cancel_orders_list = [str(x) for x in cancel_orders_list]
                close_tg_reply += 'The next TPorders was canceled by succesfully:\n' + ', '.join(byStr_cancel_orders_list) + '\n'
            if unSuccess_cancel_orders_list:
                byStr_unSuccess_cancel_orders_list = [str(x) for x in unSuccess_cancel_orders_list]
                close_tg_reply += 'The next TPorders was NOT canceled by succesfully:\n' + ', '.join(byStr_unSuccess_cancel_orders_list) + '\n'
        except Exception as ex:
            logging.exception(
                f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

        return close_tg_reply
                
class TG_MANAGER(TG_ASSISTENT):
    def __init__(self):
        super().__init__()

    def run(self):  
        try:          
            @self.bot.message_handler(commands=['start'])
            @self.bot.message_handler(func=lambda message: message.text == 'START')
            def handle_start_input(message):
                if self.block_acess_flag:
                    response_message = "Don't bullshit!"
                    message.text = self.connector_func(message, response_message)
                else:
                    self.init_itits() 
                    self.start_day_date = self.date_of_the_month()          
                    self.bot.send_message(message.chat.id, "Please enter a secret token...", reply_markup=self.menu_markup)                   
                    self.start_flag = True

            @self.bot.message_handler(func=lambda message: self.start_flag)
            def handle_start_redirect(message):
                try:
                    cur_day_date = None                    
                    value_token = message.text.strip()
                    cur_day_date = self.date_of_the_month()

                    if self.start_day_date != cur_day_date:
                        self.start_day_date = cur_day_date
                        self.block_acess_flag = False 
                        self.block_acess_counter = 0

                    if value_token == self.seq_control_token and not self.block_acess_flag:
                        self.seq_control_flag = True 
                        print(self.seq_control_flag)
                        try: 
                            response_message = "Token verification was successful! Please select an option!"
                            message.text = self.connector_func(message, response_message)  
                            self.start_flag = False        
                        except Exception as ex:
                            logging.exception(
                                f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
                            
                    elif value_token != self.seq_control_token and not self.block_acess_flag:
                        self.dont_seq_control = True
                        print(self.dont_seq_control)
                        try:
                            self.block_acess_counter += 1
                            if self.block_acess_counter >= 3:
                                self.block_acess_flag = True
                                self.start_flag = False 
                                response_message = "The number of attempts has been exhausted. Please try again later..."
                                message.text = self.connector_func(message, response_message)
                            else:
                                response_message = "Please put a valid token!"
                                message.text = self.connector_func(message, response_message)
                        except Exception as ex:
                            logging.exception(
                                f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
                except Exception as ex:
                    logging.exception(
                        f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
            # ////////////////////////////////////////////////////////////////////////////////////////////////
            
            @self.bot.message_handler(func=lambda message: message.text == 'TOP_COINS' and self.seq_control_flag and not self.block_acess_flag)
            def handle_seq5(message): 
                try:
                    top_coins = None    
                    response_message = "Please waiting..."
                    message.text = self.connector_func(message, response_message)
                    top_coins = self.assets_filters()
                    top_coins = [f"{link_emoji} https://www.coinglass.com/tv/Binance_{x}" for x in top_coins]
                    response_message = ""
                    if top_coins:
                        # response_message = str(top_coins)[2:-2].replace("', '", " ")
                        response_message = f"{money_emoji} {money_emoji} {money_emoji}" + '\n\n' + '\n\n'.join(top_coins) + '\n\n' + f"{money_emoji} {money_emoji} {money_emoji}"
                        message.text = self.connector_func(message, response_message)
                    else:
                        response_message = "Some problem with fetcing coins..."
                        message.text = self.connector_func(message, response_message)
                except Exception as ex:
                    logging.exception(
                        f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

            @self.bot.message_handler(func=lambda message: message.text == 'TOP_COINS')
            def handle_seq6(message): 
                try:
                    response_message = "Please tab START and put a valid token!"
                    message.text = self.connector_func(message, response_message)
                except Exception as ex:
                    logging.exception(
                        f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

            # //////////////////////////////////////////////////////////////////////////////////////////////

            @self.bot.message_handler(func=lambda message: message.text == 'GET LINK' and self.seq_control_flag and not self.block_acess_flag)
            def handle_getLink(message):
                try: 
                    top_coins = None    
                    response_message = "Please enter a symbol (e.g.: btcusdt)"
                    message.text = self.connector_func(message, response_message)
                    self.handle_getLink_redirect_flag = True
                except Exception as ex:
                    logging.exception(
                        f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

            @self.bot.message_handler(func=lambda message: message.text == 'GET LINK')
            def handle_seq7(message): 
                try:
                    response_message = "Please tab START and put a valid token!"
                    message.text = self.connector_func(message, response_message)
                except Exception as ex:
                    logging.exception(
                        f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

            @self.bot.message_handler(func=lambda message: self.handle_getLink_redirect_flag)
            def handle_getLink_redirect(message): 
                try:
                    symbol = None    
                    symbol = message.text.strip().upper()
                    response_message = f"{money_emoji} {money_emoji} {money_emoji}" + '\n\n' + f"{link_emoji} https://www.coinglass.com/tv/Binance_{symbol}" + '\n\n' + f"{money_emoji} {money_emoji} {money_emoji}"
                    message.text = self.connector_func(message, response_message)
                    self.handle_getLink_redirect_flag = False
                except Exception as ex:
                    logging.exception(
                        f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

            # ////////////////////////////////////////////////////////////////////////////////////////////////    

            @self.bot.message_handler(func=lambda message: message.text == "FILTER" and self.seq_control_flag and not self.block_acess_flag)
            def handle_filter(message): 
                try:           
                    response_message = "For filter settings please go to the params_init file (class FILTER_SET) of the working directory and change a filter options!" 
                    message.text = self.connector_func(message, response_message)                   
                except Exception as ex:
                    logging.exception(
                        f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

            @self.bot.message_handler(func=lambda message: message.text == 'FILTER')
            def handle_seq8(message): 
                try:
                    response_message = "Please tab START and put a valid token!"
                    message.text = self.connector_func(message, response_message)
                except Exception as ex:
                    logging.exception(
                        f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

            @self.bot.message_handler(func=lambda message: message.text == "RISK" and self.seq_control_flag and not self.block_acess_flag)
            def handle_filter(message):  
                try:          
                    response_message = "Please enter a risk options: tp_mode and corresponings metrics (e.g.: s 4/2) or (e.g.: a 1.2)" 
                    message.text = self.connector_func(message, response_message) 
                    self.handle_redirect_risk_flag = True
                except Exception as ex:
                    logging.exception(
                        f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
                    
            @self.bot.message_handler(func=lambda message: self.handle_redirect_risk_flag)
            def handle_filter_redirect(message):  
                try:  
                     
                    response_message = f"Please enter a valid data and check the rest of the details"
                    if message.text.split(' ')[0].strip().upper() == 'S':
                        self.tp_mode = 'S'
                        self.TP_rate = float(message.text.split(' ')[1].strip().split('/')[0].strip())
                        self.SL_ratio = float(message.text.split(' ')[1].strip().split('/')[1].strip())
                        self.risk_init()                                                                       
                        response_message = f"The following parameters have been initialised:\ntp_mode = {self.tp_mode}, TP_rate = {self.TP_rate} risk_ralations = {self.risk_ralations}"
                        self.handle_redirect_risk_flag = False
                    elif message.text.split(' ')[0].strip().upper() == 'A':
                        self.tp_mode = 'A'                                      
                        self.atr_TP_coef = float(message.text.split(' ')[1].strip())             
                        response_message = f"The following parameters have been initialised:\ntp_mode = {self.tp_mode}, atr_TP_coef = {self.atr_TP_coef}"
                        self.handle_redirect_risk_flag = False
                     
                    message.text = self.connector_func(message, response_message) 
                    
                except Exception as ex:
                    logging.exception(
                        f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
                    response_message = "Please enter a valid data and check the rest of the details. Then try again (e.g.: s 4/2) or (e.g.: a 1.2)"
                    message.text = self.connector_func(message, response_message)                    

            @self.bot.message_handler(func=lambda message: message.text == 'RISK')
            def handle_seq9(message): 
                try:
                    response_message = "Please tab START and put a valid token!"
                    message.text = self.connector_func(message, response_message)
                except Exception as ex:
                    logging.exception(
                        f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

            # /////////////////////////////////////////////////////////////////////////////////

            @self.bot.message_handler(func=lambda message: (message.text == "BUY" or message.text == "SELL") and self.seq_control_flag and not self.block_acess_flag)
            def handle_buyOrder(message): 
                try:            
                    response_message = "Please enter a coin and depo/quantity, direction with a space (e.g.: btc 12usdt 1) or (e.g.: btc 0.002btc -1)"
                    message.text = self.connector_func(message, response_message)           
                    self.open_order_redirect_flag = True  
                except Exception as ex:
                    logging.exception(
                        f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

            @self.bot.message_handler(func=lambda message: message.text == "BUY" or message.text == "SELL")
            def handle_seq3(message): 
                try:
                    response_message = "Please tab START and put a valid token!"
                    message.text = self.connector_func(message, response_message)  
                except Exception as ex:
                    logging.exception(
                        f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")       
                
            @self.bot.message_handler(func=lambda message: self.open_order_redirect_flag)
            def handle_buyOrder_redirect(message):
                symbol = None 
                depo = None
                order_esential = "ABRAKADABRA"

                buy_order_returned_list = []
                order_tg_reply = ""
                
                try:              
                    symbol = message.text.split(' ')[0].strip().upper() + 'USDT'     
                    depo = message.text.split(' ')[1].strip().upper()
                    is_selling = int(message.text.split(' ')[2].strip().upper())
                    response_message = "Please waiting..."
                    self.open_order_redirect_flag = False
                    message.text = self.connector_func(message, response_message)
                    # ///////////////////////////////////////////////////////////
                    buy_order_returned_list, enter_deFacto_price = self.buy_order_tgButton_handler(symbol, depo, is_selling)

                    if buy_order_returned_list:
                        if is_selling == 1:
                            order_esential = 'BUY'
                        elif is_selling == -1:
                            order_esential = 'SELL'
                        if 0 in buy_order_returned_list:
                            order_tg_reply += f"Some exceptions with placeing {order_esential} order..." + '\n'                        
                        if -1 in buy_order_returned_list:
                            order_tg_reply += f"Some problem with placeing {order_esential} order..." + '\n'
                        if 1 in buy_order_returned_list:
                            order_tg_reply += f"The {order_esential} order was executed successfully. Enter price = {enter_deFacto_price}" + '\n'
                    else:
                        order_tg_reply += f"Some exceptions with placeing {order_esential} order..."

                    message.text = self.connector_func(message, order_tg_reply)               
                except Exception as ex:
                    logging.exception(
                        f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
                    response_message = "Please enter a valid data and check the rest of the details. Then try again (e.g.: btc 9)"
                    message.text = self.connector_func(message, response_message)
                    self.open_order_redirect_flag = True

            # /////////////////////////////////////////////////////////////////////////////////
                    
            @self.bot.message_handler(func=lambda message: message.text == "TP" and self.seq_control_flag and not self.block_acess_flag)
            def handle_tpOrder(message):   
                try:
                    response_message = "Please select an option:\n1 - Auto;\n2 - Current"        
                    message.text = self.connector_func(message, response_message)            
                    self.tp_order_redirect_flag = True  
                except Exception as ex:
                    logging.exception(
                        f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

            @self.bot.message_handler(func=lambda message: message.text == "TP")
            def handle_seq2(message):
                try: 
                    response_message = "Please tab START and put a valid token!"
                    message.text = self.connector_func(message, response_message)
                except Exception as ex:
                    logging.exception(
                        f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

            @self.bot.message_handler(func=lambda message: self.tp_order_redirect_flag)
            def handle_tpOrder_redirect(message): 
                try:
                    self.tp_order_redirect_flag = False  
                    print(message.text)
                    response_message = ""
                    if message.text == '1':
                        response_message = "Please enter a coin (e.g.: btc) or (e.g.: eth)"
                        self.tp_order_auto_redirect_flag = True
                            
                    elif message.text == '2':
                        response_message = "Please enter a coin, depo or quantity and target prices with a space (e.g.: btc 12usdt/45500) or (e.g.: btc 0.002btc/45500 0.002btc/46500 0.002btc/47500)"
                        self.tp_order_custom_redirect_flag = True
                    
                    message.text = self.connector_func(message, response_message)
                except Exception as ex:
                    logging.exception(
                        f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

            @self.bot.message_handler(func=lambda message: self.tp_order_auto_redirect_flag)
            def handle_tpOrder_redirect_auto(message): 
                print('bndgjklb nadgjklbn') 
                self.tp_order_auto_redirect_flag = False 
                tp_response = "Some problems with making tp order..."
                symbol = None
                target_prices = []   
                try:
                    symbol = message.text.split(' ')[0].strip().upper() + 'USDT'     
                    # depo = message.text.split(' ')[1].strip().upper()                              
                    response_message = "Please waiting..."                    
                    message.text = self.connector_func(message, response_message)    
                    tp_response = self.tp_make_orders(symbol, target_prices, self.TP_rate, self.atr_TP_coef, self.tp_mode)                               
                    message.text = self.connector_func(message, tp_response)   
                except Exception as ex:
                    logging.exception(
                        f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
                    response_message = "Please enter a valid data and check the rest of the details. Then try again (e.g.: btc 9)"
                    message.text = self.connector_func(message, response_message)
                    self.tp_order_auto_redirect_flag = True 

            @self.bot.message_handler(func=lambda message: self.tp_order_custom_redirect_flag)
            def handle_tpOrder_redirect_custom(message):  
                self.tp_order_custom_redirect_flag = False
                symbol = None
                target_prices = []
                tp_response = ""
                try:
                    dataa = message.text.strip().split(' ')
                    symbol = dataa[0].upper() + 'USDT'                   
                    target_prices = dataa[1:]
                    print(symbol)
                    print(target_prices)

                    response_message = "Please waiting..."                    
                    message.text = self.connector_func(message, response_message)  
                    tp_response = self.tp_make_orders(symbol, target_prices, self.TP_rate, self.atr_TP_coef, self.tp_mode)                   
                    message.text = self.connector_func(message, tp_response)  
                except Exception as ex:
                    logging.exception(
                        f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

                           

            # /////////////////////////////////////////////////////////////////////////////////            

            @self.bot.message_handler(func=lambda message: message.text == "BOOK" and self.seq_control_flag and not self.block_acess_flag)
            def handle_book(message): 
                try:              
                    response_message = "Please enter a ticker and all_tikers_flag (e.g.: btc n) or (e.g.: fjkl y)"
                    message.text = self.connector_func(message, response_message)
                    self.book_triger_flag = True
                except Exception as ex:
                    logging.exception(
                        f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

            @self.bot.message_handler(func=lambda message: message.text == "BOOK")
            def handle_seq1(message): 
                try:
                    response_message = "Please tab START and put a valid token!"
                    message.text = self.connector_func(message, response_message)
                except Exception as ex:
                    logging.exception(
                        f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

            @self.bot.message_handler(func=lambda message: self.book_triger_flag)
            def handle_book(message):  
                self.book_triger_flag = False    
                book_resp = False         
                symbol = None
                response_message = 'Some problems with getting trading data. "Please enter a valid data and check the rest of the details. Then try again: (e.g.: btc)'
                try:
                    symbol = message.text.split(' ')[0].strip().upper() + 'USDT'
                    all_tickers_flag = message.text.split(' ')[1].strip().upper() == 'Y'
                    book_resp = self.get_myBook(symbol, all_tickers_flag)                
                    if book_resp:
                        response_message = 'Please check the csv file in your work directory!'      

                    message.text = self.connector_func(message, response_message)
                except Exception as ex:
                    logging.exception(
                        f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
                    message.text = self.connector_func(message, response_message)         


            @self.bot.message_handler(func=lambda message: message.text == "BALANCE" and self.seq_control_flag and not self.block_acess_flag)
            def handle_getBalance(message):
                get_balance1 = ''
                get_balance2 = ''
                response_message = "Please waiting..."
                try:
                    message.text = self.connector_func(message, response_message)
                    resp_text = ""
                    get_balance1 = self.get_ccxtBinance_balance()  
                    # get_balance1 = self.get_balance()           
                    # get_balance2 = self.get_balance()
                    resp_text = get_balance1 + '\n' + str(get_balance2)
                    response_message = f"Your {self.market.upper()} balance is:\n\n{resp_text}"
                    message.text = self.connector_func(message, response_message) 
                except Exception as ex:
                    logging.exception(
                        f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
                        
            # /////////////////////////////////////////////////////////////////////////////// 
            @self.bot.message_handler(func=lambda message: message.text == "BALANCE")
            def handle_seq4(message): 
                try:
                    response_message = "Please tab START and put a valid token!"
                    message.text = self.connector_func(message, response_message) 
                except Exception as ex:
                    logging.exception(
                        f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
            # /////////////////////////////////////////////////////////////////////////////// 
                
            # @self.bot.message_handler(func=lambda message: message.text not in self.reserved_frathes_list)
            # def handle_exceptionsInput(message):
            #     try:
            #         response_message = f"Try again and enter a valid option."
            #         message.text = self.connector_func(message, response_message)   
            #     except Exception as ex:
            #         logging.exception(
            #             f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")  
            self.bot.polling()
        except Exception as ex:
            logging.exception(
                f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
                    

        
def main():
    my_bot = TG_MANAGER()
    my_bot.run()

if __name__=="__main__":
    main()
