# BINANCE AUTO TRADING SCRIPT

this a binance trading script written in python that use a
strategy that i have implemented to track rcryptopair price
, to analyse using indicators , place an order if there is
an opportunity.

Platforms supported:

- Binance
- kraken (pending)
- coinbase (near future)

Indicators implemented :

                        - RSI
                        - MACD
                        - SMA 20
                        - BOLLINGER BANDS
                        - STOCHASTIC
                        - many more to be added
Crypto tracked:

                -[ADA,BCH,BNB,BTC,ETH,LTC
                LUNA,SOL,USDT,XRP]

10 coins supported and +50 cryptopairs tracked

## RUN THE BOT

run those lines of code each one

    git clone https://github.com/mercyplaisir/tradeapp.git
    cd tradeapp
    touch .env
    nano .env

after running the last line. it should open the '.env' file and you should put in info in such order

#####  .env

    BINANCEPUBLICKEY="your binance public key"
    BINANCEPRIVATEKEY="your binance secret key"

after that you should be ready to go by running

    python3 -m virtualenv venv
    source venv/bin/activate
    pip3 install -r requirements.txt
    python3 run.py

Thanks for visiting the repos.
**Hope you enjoy.**
