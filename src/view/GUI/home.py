import tkinter




#applicatoion
mainapp = tkinter.Tk()
mainapp.minsize(1000,600)
mainapp.title("Trade app")

#==========for entering apikeys
apiLabelWidth = 50

apikeyFrame = tkinter.LabelFrame(mainapp,text="apikeys")
apiLabel = tkinter.Label(apikeyFrame,text="enter your API: ")
#Public key
publicKeyLabel = tkinter.Label(apikeyFrame,text= "Public key :")
publicKeyEntry = tkinter.Entry(apikeyFrame,width=apiLabelWidth)
#Private Key
privateKeyLabel = tkinter.Label(apikeyFrame, text="Private key :")
privateKeyEntry = tkinter.Entry(apikeyFrame, width=apiLabelWidth)

#=========================for choosing crypto
cryptoChooseFrame = tkinter.LabelFrame(mainapp,text = "choose crypto")
#crypto
cryptoChooseLabel = tkinter.Label(cryptoChooseFrame,text="choose your Basecoin:")
cryptoChooseRadio = tkinter.Radiobutton(cryptoChooseFrame,text="BTC",value=1)
cryptoChooseRadio1 = tkinter.Radiobutton(cryptoChooseFrame,text="USDT",value=0)












#======================pack process=============
apikeyFrame.grid(sticky="nw")
apiLabel.grid(row=0)
publicKeyLabel.grid(row=1,column=0,columnspan=2)
publicKeyEntry.grid(row=1, column=2)
privateKeyLabel.grid ( row=2,column=0,columnspan=2)
privateKeyEntry.grid(row=2,column=2)
#=============================================

cryptoChooseFrame.grid(sticky="w")
cryptoChooseLabel.grid(row=0)
cryptoChooseRadio.grid(row=1,column=1)
cryptoChooseRadio1.grid(row = 2,column = 1)

#==========================================







mainapp.mainloop()

