import os
import io

import telebot

# log = create_logger(__name__)

class Telegram:
    
    token = os.getenv('TOKEN')
    chat_id = os.getenv('CHATID')
    bot = telebot.TeleBot(token=token,parse_mode=None)
        
    @classmethod
    def send_message(cls,message:str):
        # cls.log.info('sending message')
        # cls.bot.send_message(chat_id=cls.chat_id, text=message)
        # print(cls.token)
        if len(message) > 4095:
            for x in range(0, len(message), 4095):
                cls.bot.send_message(cls.chat_id, text=message[x:x+4095])
        else:
            cls.bot.send_message(cls.chat_id, text=message)
    @classmethod
    def send_image(cls,bf:io.BytesIO):
        cls.bot.send_photo(cls.chat_id, bf)

    @classmethod
    def obj_to_str(cls,obj):
        """"""
