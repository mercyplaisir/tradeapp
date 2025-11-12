import os
import io
from enum import Enum

import telebot




class Telegram:
    
    def __init__(self,token:str,chat_id:str ):
        self.bot:telebot.TeleBot = telebot.TeleBot(token=token, parse_mode=None)
        self.chat_id:str  = chat_id
    
    def send_message(self,message:str):
        # cls.log.info('sending message')
        # cls.bot.send_message(chat_id=cls.chat_id, text=message)
        # print(cls.token)
        # if len(message) > 4095:
        #     for x in range(0, len(message), 4095):
        #         cls.bot.send_message(cls.chat_id, text=message[x:x+4095])
        # else:
        #     cls.bot.send_message(cls.chat_id, text=message)
        self.bot.send_message(chat_id=self.chat_id, text=message)
    
    def send_image(self,bf:io.BytesIO):
        self.bot.send_photo(self.chat_id, bf)

    @classmethod
    def obj_to_str(cls,obj):
        """"""

class TelegramChanel(Telegram):
    def __init__(self,name:str,token:str,chat_id:str):
    
        self.token = token
        self.chat_id = chat_id
        super().__init__(token=token,chat_id=chat_id)
    
    def send_message(self,message:str):
        super().send_message(message)
    def __post_init__(self):
        ...