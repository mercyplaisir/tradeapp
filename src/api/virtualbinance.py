from binanceApi import Binance



class VirtualClient(Binance):

    def __init__(self,publickey:str=None,secretkey:str = None ,coin:str = 'BTC'):
        super().__init__(publickey=publickey,secretkey=secretkey)
        
        self.coin = coin

        pass
    


    def passOrder(self,cryptopair):
        decision = self._basecoin_or_quotecoin(cryptopair = cryptopair,coin=self.coin)
        if decision=='buy':
            self.buyOrder(cryptopair=cryptopair)
        elif decision=='sell':
            self.sellOrder(cryptopair= cryptopair)
    
    def _get_price(self,cryptopair:str=None):
        return self.coinPriceInfo(cryptopair)['price']
    def _get_price_change(self,cryptopair:str=None):
        return self.coinPriceInfo(cryptopair)['priceChange']

    def _buyOrder(self, cryptopair: str=None):
        priceInfo  =  self._get_price(cryptopair=cryptopair)
        
        pass
    
    
    def _sellOrder(self, cryptopair: str=None):
        pass
    

    def _getcoinsrelated(self,quotecoin:str=None,basecoin:str =None):
        #return all coins related quotecoins or basecoin
        if basecoin:
            #for basecoin you must provide a quotecoin
            self.database.selectDB("select basecoin from relationalcoin where quotecoin ='"+quotecoin+"'")
        elif quotecoin:
            #for quotecoin you must provide a basecoin
            self.database.selectDB("select quotecoin from relationalcoin where basecoin ='"+basecoin+"'")




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
            #BNBBTC from bnb to btc you sell
            return 'sell'
        elif cryptopair.endswith(coin):
            #inverse
            return 'buy'
    
    
    
