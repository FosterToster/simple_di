from typing import Generic, TypeVar, Type, Union, Callable
from ..container import BaseContainer


T = TypeVar('T')


class _Annotator(Generic[T]):
    '''
    Annotator class. For internal use only
    '''


    def __init__(self, annotator_class: Type['BaseContainer'], provider: 'BaseProvider[T]') -> None:
        self.__annotator_class__ = annotator_class
        self.__provider__ = provider


    def __provide__(self, container: 'BaseContainer') -> T:
        try:
            return self.__provider__.__provide__(container)
        except Exception as e:
            e.args = (f"[DI]{container.__class__.__name__} > {self.__provider__.__class__.__name__}", *e.args)
            raise e


    def __getattr__(self, name):
        return getattr(self.__provide__(self.__annotator_class__()), name)
            

class BaseProvider(Generic[T]):

    def __init__(self, factory: Union[Type[T], Callable[..., T]], *args, **kwargs):
        self.__factory__ = factory
        self.__args__ = args
        self.__kwargs__ = kwargs
        self.__overrider__ = None


    def __get__(self, container, annotator) -> T:
        
        if container is None:
            return self.__annotate__(annotator)
        else:
            return self.__provide__(container)


    def __set__(self, container, value):
        self.__overrider__ = value


    def __annotate__(self, annotator) -> T:
        return _Annotator(annotator, self)


    def __provide__(self, container) -> T:
        if self.__overrider__ is not None:
            if isinstance(self.__overrider__, BaseProvider):
                return self.__overrider__.__provide__(container)
            else:
                return self.__overrider__
                
        args = [ arg.__provide__(container) if isinstance(arg, BaseProvider) else arg for arg in self.__args__]
        kwargs = dict( (key, arg.__provide__(container) if isinstance(arg, BaseProvider) else arg) for key, arg in self.__kwargs__.items() )
        return self.__factory__(*args, **kwargs)

    def __getattr__(self, name):
        return SubProvider(name, self)


class SubProvider(BaseProvider[T]):
    
    def __init__(self, subfield: str, superprovider: BaseProvider):
        self.__subfield__ = subfield
        self.__superprovider__ = superprovider

    def __provide__(self, container) -> T:
        return getattr(self.__superprovider__.__provide__(container), self.__subfield__)