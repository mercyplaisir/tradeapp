#import numpy as np
import pandas as pd
from binance.client import Client
from binance.enums import *
#import math
import datetime
import time
import json
#import random
import websocket




class Binance:

    def __init__(self, apiPublickey, apiSecretkey):
        self.apikey = apiPublickey
        self.secretkey = apiSecretkey
        Client(self.apikey,self.secretkey)
        