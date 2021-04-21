
import csv
import datetime


list_of_crypto = ['BTC','ETH','XRP','BNB','OCEAN','OGN']



f = open('test.csv','w')
header = ("time,list_of_crypto\n")
f.write(header)

for i in list_of_crypto:
    f.write('{},{}\n'.format(datetime.datetime.now(),i))

f.close()


