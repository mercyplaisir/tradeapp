import tkinter


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
publicKeyEntry = tkinter.Entry(apikeyFrame,width=apiLabelWidth)
#Private Key
privateKeyLabel = tkinter.Label(apikeyFrame, text="Private key :")
privateKeyEntry = tkinter.Entry(apikeyFrame, width=apiLabelWidth)

#=========================for choosing crypto
#crypto
cryptoChooseLabel = tkinter.Label(apikeyFrame,text="choose your Basecoin:")
cryptoChooseRadio = tkinter.Radiobutton(apikeyFrame,text="BTC",value=1)
cryptoChooseRadio1 = tkinter.Radiobutton(apikeyFrame,text="USDT",value=0)

buttonFrame = tkinter.Frame(mainapp)
startButton = tkinter.Button(buttonFrame,text = "start")
stopButton = tkinter.Button(buttonFrame,text = "stop")
quitButton = tkinter.Button(buttonFrame,text = "stop and quit")

#====================crypto to trade===================

cryptoTradeLabel = tkinter.Label(apikeyFrame,text= "choose crypto to trade : ")
dogeCheck = tkinter.Checkbutton(apikeyFrame,
				 text= "DOGE",offvalue = False,onvalue =True)
ethCheck = tkinter.Checkbutton(apikeyFrame,
				 text= "ETH",offvalue = False,onvalue =True)

ltcCheck = tkinter.Checkbutton(apikeyFrame,
				 text= "LTC",offvalue = False,onvalue =True)
bchCheck = tkinter.Checkbutton(apikeyFrame,
				 text= "BCH",offvalue = False,onvalue =True)
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

