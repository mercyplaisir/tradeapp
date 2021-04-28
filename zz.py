import time 
import datetime


y=datetime.datetime.now()
x = datetime.timedelta(days=5)

z=((str(y-x).split(' '))[0]).replace('-',' ')


z=datetime.datetime.strptime(z,'%y %b %d')
print(z)

