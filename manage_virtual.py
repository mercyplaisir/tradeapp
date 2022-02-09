dd = {
    "t": 123400000,
    "o": "0.0010",
    "c": "0.0020",
    "h": "0.0025",
    "l": "0.0015",
    "v": "1000"

}
dd.copy()
d = {}

columns = ['date', 'open','close', 'high', 'low',  'volume']
keys = list(dd.keys())

for i in range(len(dd.keys())):
    column = columns[i]
    key = keys[i]
    d[column] = dd[key]
print(d)
