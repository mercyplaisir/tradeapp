# loop into list of pairs check if any oversold or overbought in 15min chart
# if overbought and i have it(worth more tha minimum order value, ex 10), i sell it

# if oversold and i dont have it, 
        # go down in 5min and BUY
        #  in oversold area
from tools.tools import settings_loader

def main():
    settings:dict = settings_loader()
    quote_crypto = settings['quote_crypto']
    cryptos = settings['crypto_list']
    # pairs = [crypto+quote_crypto for crypto in cryptos]
    for crypto in cryptos:
        pair = crypto + quote_crypto
    

if __name__ == "__main__":
    main()