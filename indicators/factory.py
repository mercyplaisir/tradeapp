from typing import Callable, Any

indicator_creation_funcs: dict[str, Callable[..., any]] = {}


def register(indicator_type: str, creation_func: Callable[..., Any]):
    """register a new indicator"""
    indicator_creation_funcs[indicator_type] = creation_func


def unregister(character_type: str):
    """unregister a indicator"""
    indicator_creation_funcs.pop(character_type, None)


def create(arguments: dict[str, any]) -> object:
    """create  a indicator of a specific type, given a dictionary of arguments"""
    args_copy = arguments.copy()
    indicator_type = args_copy.pop("type")
    try:
        creation_func = indicator_creation_funcs[indicator_type]
        return creation_func()
    except KeyError:
        raise ValueError(f"unknown indicator type {indicator_type!r}") from None

def get_indicators()->list[str]:
    return list(indicator_creation_funcs.keys())
