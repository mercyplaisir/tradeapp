from exchange import Binance

#run file
def main():
    with Binance() as client:
        client.run()
