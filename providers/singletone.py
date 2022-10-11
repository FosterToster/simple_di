from typing import Union, Type, TypeVar, Callable, Generic
from .abc import BaseProvider, T


class Singletone(BaseProvider[T]):
    
    def __init__(self, factory: Union[Type[T], Callable[..., T]], *args, **kwargs):
        self.__instance__ = None
        super().__init__(factory, *args, **kwargs)

    def __provide__(self, container) -> T:
        if self.__instance__ is None:
            self.__instance__ = super().__provide__(container)

        return self.__instance__