import tkinter
import sys
from typing import List,Dict

sys.path.append(sys.path[0]+"/../../..")
from src.controller.tools import Tool as tl,USERINPUTS


userInputs={'crypto':[],
            'basecoin':'USDT',
            'public key':'',
            'secret key':''}
crypto = userInputs['crypto'] 











minWidth = 700
minHeigth = 400

mainapp = tkinter.Tk()
mainapp.minsize(minWidth,minHeigth)
mainapp.title("Trade app")

#==========for entering apikeys

mainFrame = tkinter.LabelFrame(master=mainapp)#,height=100,width=500)
mainFrame.place(x=10,y=10)

def api_key(appframe:tkinter.Frame):
    def KeyUpdate(*args):
        userInputs['public key'] = publicKey.get()
        userInputs['secret key'] = privateKey.get()
        tl.rewrite_json(USERINPUTS,userInputs) 
        print(userInputs)
    
    apiLabelWidth = 30

    apiLabel = tkinter.Label(appframe,text="enter your API: ")
    #Public key
    publicKeyLabel = tkinter.Label(appframe,text= "Public key :")

    publicKey = tkinter.StringVar()
    publicKey.trace("w",KeyUpdate)
    publicKeyEntry = tkinter.Entry(appframe,show='*',textvariable = publicKey,width=apiLabelWidth)

    #Private Key
    privateKeyLabel = tkinter.Label(appframe, text="Private key :")

    privateKey = tkinter.StringVar()
    privateKey.trace("w",KeyUpdate)

    privateKeyEntry = tkinter.Entry(
        appframe,
        show='o',
        textvariable = privateKey,
        width=apiLabelWidth)

    
    #======================pack process=============
    
    apiLabel.grid(column=0)
    publicKeyLabel.grid(row=1,column=0,columnspan=2)
    publicKeyEntry.grid(row=1, column=2)
    privateKeyLabel.grid ( row=2,column=0,columnspan=2)
    privateKeyEntry.grid(row=2,column=2)


#=========================for choosing crypto
def choose_basecoin(appframe:tkinter.Frame):
    def BaseCoinValue(*args):
        userInputs["basecoin"]='BTC' if cryptoChooseValue.get()==1 else 'USDT'
        tl.rewrite_json(USERINPUTS,userInputs) 
        print(userInputs)
    
    #crypto
    cryptoChooseLabel = tkinter.Label(appframe,text="choose your Basecoin:")

    cryptoChooseValue = tkinter.IntVar()
    cryptoChooseValue.trace("w",BaseCoinValue)

    cryptoChooseRadio = tkinter.Radiobutton(appframe,text="BTC",value=1,variable = cryptoChooseValue)
    cryptoChooseRadio1 = tkinter.Radiobutton(appframe,text="USDT",value=0,variable = cryptoChooseValue)
    cryptoChooseLabel.grid()
    cryptoChooseRadio.grid(column=1)
    cryptoChooseRadio1.grid(column = 1)


#====================crypto to trade===================

def crypto_to_trade(appframe:tkinter.Frame):
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

        tl.rewrite_json(USERINPUTS,userInputs) 
        print(userInputs)


    cryptoTradeLabel = tkinter.Label(appframe,text= "choose crypto to trade : ")

    dogeSelected = tkinter.BooleanVar()
    dogeSelected.trace("w",cryptoValuee)
    ethSelected = tkinter.BooleanVar()
    ethSelected.trace("w",cryptoValuee)
    ltcSelected = tkinter.BooleanVar()
    ltcSelected.trace("w",cryptoValuee)
    bchSelected= tkinter.BooleanVar()
    bchSelected.trace("w",cryptoValuee)

    dogeCheck = tkinter.Checkbutton(appframe,
            text= "DOGE",offvalue = False,onvalue =True,variable=dogeSelected)#,variable=cryptoBool)
    ethCheck = tkinter.Checkbutton(appframe,
            text= "ETH",offvalue = False,onvalue =True,variable=ethSelected)

    ltcCheck = tkinter.Checkbutton(appframe,
            text= "LTC",offvalue = False,onvalue =True,variable =ltcSelected)
    bchCheck = tkinter.Checkbutton(appframe,
            text= "BCH",offvalue = False,onvalue = True,variable =bchSelected)
    cryptoTradeLabel.grid(column=0)
    checkcol=1
    dogeCheck.grid(column =checkcol)
    ethCheck.grid(column =checkcol)
    ltcCheck.grid(column = checkcol)
    bchCheck.grid(column = checkcol)
    pass




def main_button(appframe:tkinter.Frame):
    buttonFrame = tkinter.Frame(appframe)
    startButton = tkinter.Button(buttonFrame,text = "start")
    stopButton = tkinter.Button(buttonFrame,text = "stop")
    quitButton = tkinter.Button(buttonFrame,text = "stop and quit")

    buttonFrame.place(x=465,y=365)
    startButton.grid(row=0,column=0)
    stopButton.grid(row=0,column=1)
    quitButton.grid(row=0,column=3)







        
#======================P/L========================
def profit_loss(appframe:tkinter.Frame):
    plFrame = tkinter.LabelFrame(appframe,text= "P/L")

    plLabel=tkinter.Label(plFrame, text="Profit/Loss",width=20)

    showPlLabel=tkinter.Label(plFrame, text="{+2}%")
    
    plFrame.place(x=500,y=1)
    plLabel.grid()
    showPlLabel.grid()
#==============================Buttons==============================




#=============================================


#==========================================
api_key(mainFrame)
choose_basecoin(mainFrame)
crypto_to_trade(mainFrame)
main_button(mainapp)
profit_loss(mainapp)


#============================================
#===============================


mainapp.mainloop()

