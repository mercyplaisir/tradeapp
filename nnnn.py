llll ={'USD':'20','BTC':'534'}

def balance_restructure(data):
    result = ''
    items = data.items()
    for item in items:
        coin,balance = item
        result += f'{coin} : {balance} \n'
    return result
print(balance_restructure(llll))