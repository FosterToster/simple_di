# Simple dependency injection
It keeps intellisense and doesn't needs any wirings/decorators


New container exapmle:
```python
# base class for containers
from simple_di import BaseContainer

# Some providers
from simple_di import Singletone, Factory, Dummy

# Note that providers are working only with classes.
# Do not try to use primitive types as container values

# Test class
class Some:
    def __init__(self, args):
        ...

class App(BaseContainer):


    # Singletone DI provider guarantees that "Some" 
    # will be instanced once with passed args/kwargs 
    # and the same instance will be available for each dependency usage
    some = Singletone(Some, "hello", "world") 


    # Factory DI provider will create new instance of "Some" 
    # with passed args/kwargs each time when dependency will be used
    more = Factory(Some, "hello", "world")

    # Dummy provider just requires to be overriden.
    # Passed type will be never instanced, but will be used for intellisense.
    much_more = Dummy(Some)

```

Container usage example
```python

# with function
def some_frequently_referenced_func(required_arg, *, required_kwarg, dependency = App.some):
    # intellisense for "dependency" will work here.
    ...

# with classes
class SomeController:
    def __init__(self, dependency = App.more):
        self.dep = dependency

```