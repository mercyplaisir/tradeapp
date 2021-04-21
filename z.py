import csv
import json
import time
import datetime




now_time = datetime.datetime.now()

now_time = now_time.strftime("%d-%b-%Y (%H:%M:%S.%f)")

print(type(now_time))

print(now_time)
text={'coin':'text'}

i={'hello':'word'}




def write_json(text):
    
    with open('./test.json','r') as f:
        j = json.load(f)
        j.append(text)
    with open('./test.json','w') as f:
        json.dump(j,f,indent= 4)

        

        
        

write_json(text)



write_json(i)






