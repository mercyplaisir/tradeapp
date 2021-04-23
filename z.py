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



i=0.0100012
x = percent_calculator(i,2)

#y=percent_change(i,)

print(x)
#print(y)

i = 0

def foo():
    i = 1
    print(i)

foo()
print(i)