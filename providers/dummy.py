from .abc import BaseProvider, T

class Dummy(BaseProvider[T]):

    def __provide__(self, container) -> T:
        if self.__overrider__ is None:
            raise ReferenceError(f'All Dummy providers must be overriden on first container initialization')
        
        return super().__provide__(container)