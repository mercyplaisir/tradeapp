from typing import Dict,List, Protocol

from tradeapp.errors import CryptoNotInExchange
from tradeapp.exchanges.binancef.tools import aobject
class Exchange(Protocol):
    async def load_markets(reload:bool) -> None:
        ...
    async def fetch_balance(currency:str) -> Dict:
        ...

class Crypto(aobject):

    
    async def __init__(self, name: str, ex: Exchange) -> None:
        
        self.name = name
        self.ex = ex
        await self._check()
    async def __new__(cls,*args, **kwargs):
        return await super().__new__(cls,*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name}"

    @property
    def balance(self) -> float | int:
        return self._balance()[0]

    @property
    def locked(self) -> float | int:
        pass

    @property
    def total(self) -> float | int:
        pass

    async def _check(self):
        if not self.ex.symbols:
            await self.ex.load_markets(True)
        for _,key in enumerate(await self.ex.load_markets()):
            if self.name in key:
                return
        raise CryptoNotInExchange(f'{self.name} not in the exchange')


    def _balance(self):
        data: Dict[str, float | int] = self.get_balance()
        free, used, total = data.values()
        return free, used, total

    async def get_balance(self) -> Dict:
        return await self.ex.fetch_balance(currency=self.name)
    async def get_cryptopair_related(self):
        data:str = [key for _,key in enumerate(await self.ex.load_markets()) if self.name in key]
        res = [d for d in data if  (':' not in d )]
        return res

