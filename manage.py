from exchanges import Binance

#run file
def main():
    with Binance() as client:
        client.run()
