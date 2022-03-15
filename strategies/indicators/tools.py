"""Tools for indicators"""
from typing import Literal

COUNT_START = 5 # for indicators study



def count_for_decision(
    true_count: int, false_count: int, buy_condition: bool = True
) -> Literal['buy','sell','wait']:

    
    count_for_dec = COUNT_START // 2 + 1
    count_for_wait = COUNT_START // 2
    if true_count >= count_for_dec and buy_condition:
        return "buy"
    elif false_count >= count_for_dec:
        return "sell"
    elif true_count==count_for_wait or false_count==count_for_wait :
        return "wait"
        # return f"truecount:{true_count}, falsecount:{false_count} "
