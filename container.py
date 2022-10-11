
class BaseContainer:
    '''
    Base container class to inherit from.
    Every container is a singletone
    '''
    
    __instance__ = None

    def __initialize__(self, class_, **overrides):
        for key in vars(class_).keys():
            if key in overrides:
                setattr(self, key, overrides[key])


    def __new__(class_, **overrides):
        if class_.__instance__ is None:
            class_.__instance__ = super().__new__(class_)
            class_.__instance__.__initialize__(class_, **overrides)

        return class_.__instance__