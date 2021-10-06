"""Meta-class of Constant."""

from itertools import filterfalse

from constant.exc import ConstantError


class ConstantMeta(type):
    """Meta-class of Constant."""

    _definition_only = False

    def __new__(mcls, classname, bases, dict):
        """Magic method."""
        # Prohibit inheritance of different ConstantMeta.
        const_bases = [cls for cls in bases if isinstance(cls, ConstantMeta)]
        for cmp_cls in const_bases[1:]:
            if type(const_bases[0]) != type(cmp_cls):
                fst_name = const_bases[0].__name__
                cmp_name = cmp_cls.__name__
                raise ConstantError(f"Can't inheritance of [{fst_name}] and [{cmp_name}] together") # noqa

        # Prohibits class-variable collision.
        super_consts = set()
        for base_cls in bases:
            base_consts = mcls.__get_constant_attr(base_cls.__dict__)
            collision_consts = (super_consts & base_consts)
            if collision_consts:
                collisions = ", ".join(collision_consts)
                bname = base_cls.__name__
                raise ConstantError(f"Constant [{collisions}] conflicts when inheriting class [{bname}]") # noqa
            super_consts |= base_consts

        # Prohibits class-variable redefinition.
        new_consts = mcls.__get_constant_attr(dict)
        rebind_consts = (super_consts & new_consts)
        if rebind_consts:
            rebinds = ", ".join(rebind_consts)
            raise ConstantError(f"Can't redefine constant [{rebinds}]")

        # Prohibit instantiation of Constant class.
        # NOTE: Replacing __init__ function.
        def _meta__init__(self, *args, **kwargs):
            raise ConstantError("Can't make instance of Constant class")
        dict["__init__"] = _meta__init__

        return type.__new__(mcls, classname, bases, dict)

    @classmethod
    def __get_constant_attr(mcls, dict):
        """Get a set of constant attributes that are treated as constants."""
        # Gets a set of attributes other than magic attribute like __str__.
        attributes = set(atr for atr in dict)
        attributes = set(filterfalse(ConstantMeta.__is_magic_attr, attributes))
        # Gets a set of attributes that are treated as constants.
        constant_attr = set(filter(mcls._is_constant_attr, attributes))
        # Gets a set of settable attributes.
        settable_attr = set(filter(mcls._is_settable_attr, attributes))
        # Gets a set of non-constant and non-settable attributes.
        indefinite_attr = attributes - (constant_attr | settable_attr)
        if indefinite_attr:
            indefinites = ", ".join(indefinite_attr)
            raise ConstantError(f"Attribute [{indefinites}] is not constant or not settable.") # noqa
        return constant_attr

    @staticmethod
    def __is_magic_attr(name):
        """Determine if the attribute name is a magic attribute."""
        return name.startswith("__") and name.endswith("__")

    @classmethod
    def _is_constant_attr(mcls, name):
        """Determine if the attribute name is treated as a constant."""
        return True

    @classmethod
    def _is_settable_attr(mcls, name):
        """Determine if the attribute name is treated as a settable."""
        return (not mcls._is_constant_attr(name))

    def __setattr__(cls, name, value):
        """Get the meta-class of cls."""
        mcls = type(cls)
        if mcls._is_constant_attr(name) or (not mcls._is_settable_attr(name)):
            raise ConstantError(f"Can't set attribute [{name}] to Constant")
        else:
            super().__setattr__(name, value)
