import csv
import json
import time
import datetime
import math





def percent_calculator(x:float,y:str):
    z=x+((x*y)/100)
    return z
def percent_change(original_number:float,new_number:float):
    z = ((new_number-original_number)/original_number)*100
    return z



i=0.047012
x = percent_calculator(i,0.4)

#y=percent_change(i,)

y = percent_change(i,0.047186)
   


print(x)
print(y)




