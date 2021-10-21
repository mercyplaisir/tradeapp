from datetime import datetime
from .binanceApi import Binance



class VirtualClient(Binance):

    def __init__(self,publickey:str=None,secretkey:str = None ,coin:str = None):
        super().__init__(publickey=publickey,secretkey=secretkey,coin=coin)
        

    def passOrder(self,cryptopair:str):
        cryptopair=cryptopair
        basecoin_or_quotecoin = self._basecoin_or_quotecoin(cryptopair = cryptopair,coin=self.coin)
        price  =  self._get_price(cryptopair=cryptopair)
        coin_for_order = self._getBasecoin_cryptopair(cryptopair)
        quantity = self.orderQuantity(coin_for_order)


        if basecoin_or_quotecoin=='quotecoin':
            #BNBBTC from btc to bnb you buy
            self._buyOrder(
                quantity=quantity,
                coin_for_order=coin_for_order,
                action='buy',
                price = price
            )
        elif basecoin_or_quotecoin=='basecoin':

            #BNBBTC from bnb to btc you sell
            self._sellOrder(
                quantity=quantity,
                coin_for_order=coin_for_order,
                action= 'sell',
                price = price
            )
    
    



    def _buyOrder(self,**kwargs):
        """Virtual buy"""
        #modify 'virtualbalance' table
            #create new balance for the new crypto
        self.database.requestDB(f"UPDATE virtualbalance SET Balance = {kwargs['quantity']} where shortname = {kwargs['coin_for_order']} ")
            #delete balance on crypto i use to hold
        self.database.requestDB(f"UPDATE virtualbalance SET Balance = {0} where shortname = {self.coin} ")
        #modify 'virtualtrade' table
        self.database.requestDB(
            f"insert into virtualtrade(basecoin ,quotecoin,ordertype,quantity,tradetime) values('{kwargs['coin_for_order']}','{self.coin}','{kwargs['action']}','{kwargs['quantity']}','{str(datetime.now())}') ")
        #swap crypto
        self.coin = kwargs["coin_for_order"]


    def _sellOrder(self,**kwargs):
        """Virtual sell"""
        #modify 'virtualbalance' table
            #create new balance for the new crypto
        self.database.requestDB(f"UPDATE virtualbalance SET Balance = {kwargs['quantity']} where shortname = {kwargs['coin_for_order']} ")
            #delete balance on crypto i use to hold
        self.database.requestDB(f"UPDATE virtualbalance SET Balance = {0} where shortname = {self.coin} ")
        #modify 'virtualtrade' table
        self.database.requestDB(
            f"insert into virtualtrade(basecoin ,quotecoin,ordertype,quantity,tradetime) values('{kwargs['coin_for_order']}','{self.coin}','{kwargs['action']}','{kwargs['quantity']}','{str(datetime.now())}') ")
        #swap crypto
        self.coin = kwargs["coin_for_order"]
    

    def _getcoinsrelated(self,coin:str):
        #return all coins related quotecoins or basecoin
        
        infos = self.database.selectDB("select quotecoin from relationalcoin where basecoin ='"+coin+"'")
        basecoins = [info[0] for info in infos]
        
    
        
        infos = self.database.selectDB("select basecoin from relationalcoin where quotecoin ='"+coin+"'")
        quotecoins = [info[0] for info in infos]
        
        return {'quotecoins':quotecoins,'basecoins':basecoins}
    
    def _get_crypto_pair_related(self,coin:str=None):
        cryptoinfo = self.database.selectDB("select cryptopair from relationalcoin where basecoin ='"+coin+"'or quotecoin='"+coin+"'")
        
        cryptoinfo = [crypto[0] for crypto in cryptoinfo]
        return list(dict.fromkeys(cryptoinfo))


    def _getBasecoin_cryptopair(self,cryptopair):
        #sqlcon = mysqlDB()
        nn = self.database.selectDB(f"select  basecoin from relationalcoin where cryptopair='"+cryptopair+"'")
        if isinstance(nn,list) and len(nn)!=0:
            return nn[0][0]
        elif len(nn)==0:
            return 'result not found'
    
    def _getQuotecoin_cryptopair(self,cryptopair):
        #sqlcon = mysqlDB()
        nn = self.database.selectDB(f"select  quotecoin from relationalcoin where cryptopair='"+cryptopair+"'")
        if isinstance(nn,list) and len(nn)!=0:
            return nn[0][0]
        elif len(nn)==0:
            return 'result not found'
    

    def _basecoin_or_quotecoin(self,cryptopair:str=None,coin:str=None):
        if cryptopair.startswith(coin):
            
            return 'basecoin'
        elif cryptopair.endswith(coin):
            
            return 'quotecoin'
    
    
    
