import json




"""
functions in  this file:
                        
                        - write_json
                        - read_json
                        - percent_calculator
                        - percent_change

"""



BASECOIN ="BTC"







class Tool:

    baseCoin = "BTC"


    haveBaseCoin = True  # have basecoin
    Have_other_coin = False  # don't have basecoin,meaning i have a crypto

    show_trade_info = False  # pour montrer les infos sur le terminal

    sell_order = False
    buy_order = False

    coinGoodForUse = False


    profit_target_price = 0  # mon take profit price
    loss_target_price = 0  # mon stop loss price
    bought_at = 0  # le prix auxquelle j'ai achete
    now_price = 0  # prix actuelle
    percent_of_profit = 0  # percent iim making in a trade


    search_coin = True

    #---------------------------------------------------------------

    #---------------------------------------------------------------

    time_when_passing_order = 0
    time_now = 0
    time_passed_in_trade = 0


    @staticmethod
    def write_json(filename:str ,text):
        """ Write in a json file

            give parameters:
                            -filename(and path)
                            -text put in the file
        
        """

        with open(f'./{filename}', 'r') as f:
            j = json.load(f)
            j.append(text)
        with open(f'./{filename}', 'w') as f:
            json.dump(j, f, indent=4)

        print(f"saved in {filename} ")

    
    @staticmethod
    def read_json(filename:str):
        """
        read a json file

        give parameters:
                        -filename(with path)
        """
        with open(f'./{filename}', 'r') as f:
            j = json.load(f)
        
        return j


    @staticmethod
    def percent_calculator(number: float, percentage: float):
        """
        calcule d'un nombre par rapport a un pourcentage du nombre d'origine
        """
        z = number+((number*percentage)/100)
        return z

    @staticmethod
    def percent_change( original_number: float, new_number: float):
        """
        variation du prix en pourcentage entrer 2nombres
        """
        z = ((new_number-original_number)/original_number)*100
        return z

    @staticmethod
    def input_int(text):
        """veuiller entrez un texte qui sera affiche"""
        while True:
            try:
                x=int(input(text))
                break
            except:
                pass
    
    @staticmethod
    def input_str(text):
        """veuiller entrez un texte qui sera affiche"""
        while True:
            try:
                x = str(input(text))
                break
            except:
                pass
    
