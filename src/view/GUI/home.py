import tkinter


mainapp = tkinter.Tk()
mainapp.minsize(1000,600)
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




#=======Profit/Loss=========================
plFrame = tkinter.LabelFrame(mainapp,text= "P/L")
plFrameLabel = tkinter.Label(plFrame, text = "Profit/Loss")

plshowLabel = tkinter.Label(plFrame, text = "{+2}%")



#======================pack process=============
apikeyFrame.place(x=100,y=100)
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
#=========================================
plFrame.place(x=700,y=100)
plFrameLabel.grid()
plshowLabel.grid()




mainapp.mainloop()

