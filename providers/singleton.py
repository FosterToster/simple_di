from typing import Union, Type, TypeVar, Callable, Generic
from .abc import BaseProvider, T


class Singleton(BaseProvider[T]):
    
    def __init__(self, factory: Union[Type[T], Callable[..., T]], *args, **kwargs):
        self.__initialized_instance__ = None
        super().__init__(factory, *args, **kwargs)

    def __provide__(self, container) -> T:
        if self.__initialized_instance__ is None:
            self.__initialized_instance__ = super().__provide__(container)

        return self.__initialized_instance__