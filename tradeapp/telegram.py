import os
import telebot



class Telegram:
    
    token = os.getenv('TOKEN')
    chat_id = os.getenv('CHATID')
    bot = telebot.TeleBot(token=token,parse_mode=None)
        
    @classmethod
    def send_message(cls,message:str):
        print(cls.chat_id)
        cls.bot.send_message(chat_id=cls.chat_id, text=message)
    @classmethod
    def send_image(cls,path:str):
        cls.bot.send_photo()
