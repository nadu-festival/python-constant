# python-constant
This is modules to define class variables as immutable variable.

## How to use

## Install
1. Clone this repository.
  ```
  git clone https://github.com/nadu-festival/python-constant
  ```
2. Run setup.py
  ```
  cd python-constant
  python setup.py install
  ```
That's all.

## How to use
1. Define your constant class in your code.
  ```Python
  from constant import Constant

  class MyConstant(Constant):
    FOO = "foo"
    BAR = "bar"
  ```
2. Using class as constant sets.
  ```Python
  # Can't make instance.
  myconstant = MyConstant()
  # => constant.exc.ConstantError: Can't set attribute [FOO] to Constant

  # Refer the variables.
  print(MyConstant.FOO) # => foo
  print(MyConstant.BAR) # => bar

  # Can't rebind the variables.
  MyConstant.FOO = "new_foo"
  # => constant.exc.ConstantError: Can't set attribute [FOO] to Constant
  ```
3. Inheritance is supported.
  ```Python
  from constant import Constant

  class MyConstantFOO(Constant):
    FOO = "foo"

  class MyConstantFOOBAR(Constant):
    BAR = "bar"

  print(MyConstantFOOBAR.FOO) # => foo
  print(MyConstantFOOBAR.BAR) # => bar
  ```

## Customization
You can customize the Constant class by creating a subclass of ConstantMeta.

### Example1: Constant variable name must be uppercase only
```Python
from constant import ConstantMeta

# Define subclass of ConstantMeta.
class UppercaseConstantMeta(ConstantMeta):

  # override the class methods.
  @classmethod
  def _is_constant_attr(mcls, name):
    return name.isupper()

# Defines a class whose meta-class is UppercaseConstantMeta.
class UppercaseConstant(metaclass=UppercaseConstantMeta):

  FOO = "is immutable"
  bar = "is mutable"

# In this case, all lowercase attributes are mutable variable.
UppercaseConstant.bar = "overwrite bar"
print(UppercaseConstant.bar) # => overwrite bar
```

### Example2: Constant variable names must be uppercase only, and other attributes are prohibited
```Python
from constant import ConstantMeta

# Define subclass of ConstantMeta.
class RestrictedConstantMeta(ConstantMeta):

  # override the class methods.
  @classmethod
  def _is_constant_attr(mcls, name):
    return name.isupper()

  @classmethod
  def _is_settable_attr(mcls, name):
    return False

# In this case, fail to define RestrictedConstant class.
class RestrictedConstant(metaclass=RestrictedConstantMeta):

  FOO = "is immutable"
  bar = "is mutable"

# => constant.exc.ConstantError: Attribute [bar] is not constant or not settable.
```
