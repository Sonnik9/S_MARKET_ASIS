from API_BINANCE.utils_api import UTILS_APII
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
        self.settings_tg_flag = False
        self.settings_1_redirect_flag = False
        self.settings_2_redirect_flag = False
        self.order_triger = False
        self.open_order_redirect_flag = False
        self.handle_getLink_redirect_flag = False

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
    
    def tp_order_tgButton_handler(self, symbol, target_price, qnt):
        # item = self.tp_make_orders(item)
        # if item["done_level"] == 1:
        #     buy_order_returned_list.append(2)   
        # else:
        #     buy_order_returned_list.append(-2) 
        pass
    
    def buy_order_tgButton_handler(self, symbol, depo):
        item = {}  
        buy_order_returned_list = []
        try:
            # pass
            item["symbol"] = symbol
            item['is_selling'] = False
            item['qnt'] = None 
            item["recalc_depo"] = None 
            item["price_precision"] = None 
            item["tick_size"] = None
            item["atr"] = None
            item["current_price"] = self.get_current_price(symbol)
            print(f'item["current_price"]: {item["current_price"]}')
            
            if self.atr_TP_flag:
                timeframe = '15m'
                limit = 100
                m1_15_data = self.get_ccxtBinance_klines(symbol, timeframe, limit)            
                m1_15_data['TR'] = abs(m1_15_data['High'] - m1_15_data['Low'])
                m1_15_data['ATR'] = m1_15_data['TR'].rolling(window=14).mean()
                item['atr'] = m1_15_data['ATR'].iloc[-1]

            item = self.buy_market_order_temp_func(item, depo)

            if item["done_level"] == 1:
                buy_order_returned_list.append(1)
            else:
                buy_order_returned_list.append(-1)

        except Exception as ex:
            logging.exception(
                f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

            buy_order_returned_list.append(0)
            print(f"main121: {ex}")

        return buy_order_returned_list
    
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
        
        @self.bot.message_handler(commands=['start'])
        @self.bot.message_handler(func=lambda message: message.text.upper() == 'START')
        def handle_start(message):
            self.init_itits()
            self.bot.send_message(message.chat.id, "Bot start. Please, choose an option!:", reply_markup=self.menu_markup)
        # ////////////////////////////////////////////////////////////////////////////////////////////////
            
        @self.bot.message_handler(func=lambda message: message.text == 'TOP_COINS')
        def handle_topCoins(message): 
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

        # //////////////////////////////////////////////////////////////////////////////////////////////

        @self.bot.message_handler(func=lambda message: message.text == 'GET LINK')
        def handle_getLink(message): 
            top_coins = None    
            response_message = "Please enter a symbol (e.g.: btcusdt)"
            message.text = self.connector_func(message, response_message)
            self.handle_getLink_redirect_flag = True

        @self.bot.message_handler(func=lambda message: self.handle_getLink_redirect_flag)
        def handle_getLink_redirect(message): 
            symbol = None    
            symbol = message.text.strip().upper()
            response_message = f"{money_emoji} {money_emoji} {money_emoji}" + '\n\n' + f"{link_emoji} https://www.coinglass.com/tv/Binance_{symbol}" + '\n\n' + f"{money_emoji} {money_emoji} {money_emoji}"
            message.text = self.connector_func(message, response_message)
            self.handle_getLink_redirect_flag = False

        # ////////////////////////////////////////////////////////////////////////////////////////////////    

        @self.bot.message_handler(func=lambda message: message.text == "FILTER")
        def handle_filter(message):            
            response_message = "Please select a filter options..." 
            message.text = self.connector_func(message, response_message) 
            # self.handle_filter_flag = True

        @self.bot.message_handler(func=lambda message: message.text == "RISK")
        def handle_filter(message):            
            response_message = "Please select a risk options..." 
            message.text = self.connector_func(message, response_message) 
            # self.handle_risk_flag = True

        # /////////////////////////////////////////////////////////////////////////////////

        @self.bot.message_handler(func=lambda message: message.text == "BUY")
        def handle_buyOrder(message):             
            response_message = "Please enter a coin and depo/quantity with a space (e.g.: btc 12usdt) or (e.g.: btc 0.002btc)"
            message.text = self.connector_func(message, response_message)
            self.order_triger = True
            self.open_order_redirect_flag = True           
            
        @self.bot.message_handler(func=lambda message: self.open_order_redirect_flag)
        def handle_buyOrder_redirect(message):
            symbol = None 
            depo = None

            buy_order_returned_list = None
            order_tg_reply = ""
            
            try:              
                symbol = message.text.split(' ')[0].strip().upper() + 'USDT'     
                depo = message.text.split(' ')[1].strip().upper()
                response_message = "Please waiting..."
                message.text = self.connector_func(message, response_message)
                # ///////////////////////////////////////////////////////////
                buy_order_returned_list = self.buy_order_tgButton_handler(symbol, depo)

                if buy_order_returned_list:
                    if 0 in buy_order_returned_list[0]:
                        order_tg_reply += "Some exceptions with placeing order..." + '\n'                        
                    if -1 in buy_order_returned_list[0]:
                        order_tg_reply += "Some problem with placeing order..." + '\n'
                        message.text = self.connector_func(message, order_tg_reply)
                    # if -2 in buy_order_returned_list[0]:
                    #     order_tg_reply = "Some problem with setting takeProfit..." + '\n'
                    #     message.text += self.connector_func(message, order_tg_reply)
                    if 1 in buy_order_returned_list[0]:
                        order_tg_reply += "The order was created successuly!" + '\n'
                        message.text = self.connector_func(message, order_tg_reply)
                    # if 2 in buy_order_returned_list[0]:
                    #     order_tg_reply += "The takeProfit was setting successuly!" + '\n'
                else:
                    order_tg_reply += "Some exceptions with placeing order..."

                message.text = self.connector_func(message, order_tg_reply)
                self.open_order_redirect_flag = False
                
            except:
                response_message = "Please enter a valid data. Try again (e.g.: btc 9)"
                message.text = self.connector_func(message, response_message)
                self.open_order_redirect_flag = True

        # /////////////////////////////////////////////////////////////////////////////////
                
        @self.bot.message_handler(func=lambda message: message.text == "SELL")
        def handle_buyOrder(message):             
            response_message = "Please enter a coin and quantity with a space (e.g.: btc 0.004)"
            message.text = self.connector_func(message, response_message)
            # self.order_triger = True
            # self.sell_order_redirect_flag = True 

        # /////////////////////////////////////////////////////////////////////////////////
            

        @self.bot.message_handler(func=lambda message: message.text == "BOOK")
        def handle_book(message):               
            response_message = "Project in progress..."
            message.text = self.connector_func(message, response_message)
            # self.book_triger_flag = True


        @self.bot.message_handler(func=lambda message: message.text == "BALANCE")
        def handle_getBalance(message):
            get_balance1 = ''
            get_balance2 = ''
            response_message = "Please waiting..."
            try:
                message.text = self.connector_func(message, response_message)
                resp_text = ""
                get_balance1 = self.get_ccxtBinance_balance()           
                # get_balance2 = self.get_balance()
                resp_text = get_balance1 + '\n' + str(get_balance2)
                response_message = f"Your {self.market.upper()} balance is:\n\n{resp_text}"
                message.text = self.connector_func(message, response_message) 
            except Exception as ex:
                logging.exception(
                    f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
                    
        # /////////////////////////////////////////////////////////////////////////////// 
        # /////////////////////////////////////////////////////////////////////////////// 
            
        @self.bot.message_handler(func=lambda message: message.text not in self.reserved_frathes_list)
        def handle_exceptionsInput(message):
            response_message = f"Try again and enter a valid option."
            message.text = self.connector_func(message, response_message)                 

        self.bot.polling()

def main():
    my_bot = TG_MANAGER()
    my_bot.run()

if __name__=="__main__":
    main()
