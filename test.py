class Hello:
    def __init__(self) -> None:
        pass
    def __enter__(self):
        print('enter')
        return self
    def salute(self):
        print('hello')
    def __exit__(self,*args, **kwargs):
        print('exited')

with Hello() as cl:
    cl.salute()