import tkinter
import sys


sys.path.append(sys.path[0]+"/../../..")
from src.controller.tools import Tool as tl,USERINPUTS


crypto = []
userInputs={}


def KeyUpdate(*args):
    userInputs['public key'] = publicKey.get()
    userInputs['secret key'] = privateKey.get()
    tl.rewrite_json(USERINPUTS,userInputs) 
    print(userInputs)

def BaseCoinValue(*args):
    userInputs['basecoin'] = "BTC" if cryptoChooseValue.get()==1 else "USDT" 
    tl.rewrite_json(USERINPUTS,userInputs) 
    print(userInputs)


def values(*args):
    print(*args)





minWidth = 700
minHeigth = 400

mainapp = tkinter.Tk()
mainapp.minsize(minWidth,minHeigth)
mainapp.title("Trade app")

#==========for entering apikeys
apiLabelWidth = 30


apikeyFrame = tkinter.LabelFrame(mainapp,text="apikeys")
apiLabel = tkinter.Label(apikeyFrame,text="enter your API: ")
#Public key
publicKeyLabel = tkinter.Label(apikeyFrame,text= "Public key :")

publicKey = tkinter.StringVar()
publicKey.trace("w",KeyUpdate)
publicKeyEntry = tkinter.Entry(apikeyFrame,textvariable = publicKey,width=apiLabelWidth)

#Private Key
privateKeyLabel = tkinter.Label(apikeyFrame, text="Private key :")

privateKey = tkinter.StringVar()
privateKey.trace("w",KeyUpdate)

privateKeyEntry = tkinter.Entry(apikeyFrame,textvariable = privateKey, width=apiLabelWidth)



#=========================for choosing crypto
#crypto
cryptoChooseLabel = tkinter.Label(apikeyFrame,text="choose your Basecoin:")

cryptoChooseValue = tkinter.IntVar()
cryptoChooseValue.trace("w",BaseCoinValue)

cryptoChooseRadio = tkinter.Radiobutton(apikeyFrame,text="BTC",value=1,variable = cryptoChooseValue)
cryptoChooseRadio1 = tkinter.Radiobutton(apikeyFrame,text="USDT",value=0,variable = cryptoChooseValue)

buttonFrame = tkinter.Frame(mainapp)
startButton = tkinter.Button(buttonFrame,text = "start")
stopButton = tkinter.Button(buttonFrame,text = "stop")
quitButton = tkinter.Button(buttonFrame,text = "stop and quit")

#====================crypto to trade===================

cryptoTradeLabel = tkinter.Label(apikeyFrame,text= "choose crypto to trade : ")

def cryptoValuee(*args):
    if dogeSelected.get() and "DOGE" not in crypto :
        crypto.append("DOGE")
    elif not dogeSelected.get() and "DOGE" in crypto:
        crypto.remove("DOGE")

    if ethSelected.get() and 'ETH' not in crypto:
        crypto.append('ETH')
    elif not ethSelected.get() and 'ETH' in crypto:
        crypto.remove('ETH')

    if ltcSelected.get() and 'LTC' not in crypto:
        crypto.append('LTC')
    elif not ltcSelected.get() and 'LTC' in crypto:
        crypto.remove('LTC')
    if bchSelected.get() and 'BCH' not in crypto:
        crypto.append('BCH')
    elif not bchSelected.get() and 'BCH' in crypto:
        crypto.remove('BCH')

    userInputs['crypto']=crypto
    tl.rewrite_json(USERINPUTS,userInputs) 
    print(userInputs)

dogeSelected = tkinter.BooleanVar()
dogeSelected.trace("w",cryptoValuee)
ethSelected = tkinter.BooleanVar()
ethSelected.trace("w",cryptoValuee)
ltcSelected = tkinter.BooleanVar()
ltcSelected.trace("w",cryptoValuee)
bchSelected= tkinter.BooleanVar()
bchSelected.trace("w",cryptoValuee)

dogeCheck = tkinter.Checkbutton(apikeyFrame,
        text= "DOGE",offvalue = False,onvalue =True,variable=dogeSelected)#,variable=cryptoBool)
ethCheck = tkinter.Checkbutton(apikeyFrame,
        text= "ETH",offvalue = False,onvalue =True,variable=ethSelected)

ltcCheck = tkinter.Checkbutton(apikeyFrame,
        text= "LTC",offvalue = False,onvalue =True,variable =ltcSelected)
bchCheck = tkinter.Checkbutton(apikeyFrame,
        text= "BCH",offvalue = False,onvalue = True,variable =bchSelected)
#======================P/L========================
plFrame = tkinter.LabelFrame(mainapp,text= "P/L")

plLabel=tkinter.Label(plFrame, text="Profit/Loss",width=20)

showPlLabel=tkinter.Label(plFrame, text="{+2}%")
#==============================Buttons==============================



yValue = 10
#======================pack process=============
apikeyFrame.place(x=10,y=yValue)
apiLabel.grid(row=0)
publicKeyLabel.grid(row=1,column=0,columnspan=2)
publicKeyEntry.grid(row=1, column=2)
privateKeyLabel.grid ( row=2,column=0,columnspan=2)
privateKeyEntry.grid(row=2,column=2)

#=============================================

cryptoChooseLabel.grid()
cryptoChooseRadio.grid(column=1)
cryptoChooseRadio1.grid(column = 1)

#==========================================
checkcol = 1
cryptoTradeLabel.grid(column=0)
dogeCheck.grid(column =checkcol)
ethCheck.grid(column =checkcol)
ltcCheck.grid(column = checkcol)
bchCheck.grid(column = checkcol)

buttonFrame.place(x=465,y=365)
startButton.grid(row=0,column=0)
stopButton.grid(row=0,column=1)
quitButton.grid(row=0,column=3)
#============================================
plFrame.place(x=500,y=yValue)
plLabel.grid()
showPlLabel.grid()
#===============================


mainapp.mainloop()

