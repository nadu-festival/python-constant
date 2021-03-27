import unittest


from constant import ConstantMeta, ConstantError


class TestConstantMeta(unittest.TestCase):

    def test_constantmeta(self):

        class UpperConstantMeta(ConstantMeta):

            @classmethod
            def _is_constant_attr(cls, name):
                return name.isupper()

        class UpperConstant(metaclass=UpperConstantMeta):

            FOO = "foo"
            BAR = "bar"

            fizz = "fizz"
            buzz = "buzz"

        with self.subTest(case="constant read"):
            self.assertEqual(UpperConstant.FOO, "foo")
            self.assertEqual(UpperConstant.BAR, "bar")
            self.assertEqual(UpperConstant.fizz, "fizz")
            self.assertEqual(UpperConstant.buzz, "buzz")

        with self.subTest(case="overwrite constant"):
            with self.assertRaises(ConstantError):
                UpperConstant.FOO = "new_foo"
            with self.assertRaises(ConstantError):
                UpperConstant.BAR = "new_bar"

        with self.subTest(case="overwrite not constant field"):
            UpperConstant.fizz = "new_fizz"
            UpperConstant.buzz = "new_buzz"
            self.assertEqual(UpperConstant.fizz, "new_fizz")
            self.assertEqual(UpperConstant.buzz, "new_buzz")

    def test_restrict_constantmeta(self):

        class RestrictedConstantMeta(ConstantMeta):

            @classmethod
            def _is_constant_attr(cls, name):
                return name.isupper()

            @classmethod
            def _is_settable_attr(cls, name):
                return False

        with self.assertRaises(ConstantError):
            class UpperConstant(metaclass=RestrictedConstantMeta):

                FOO = "foo"
                BAR = "bar"

                fizz = "fizz"
                buzz = "buzz"

    def test_collision_constantmeta(self):

        class ConstantMetaFOO(ConstantMeta):
            pass

        class ConstantMetaBAR(ConstantMetaFOO):
            pass

        class ConstantFOO(metaclass=ConstantMetaFOO):
            pass

        class ConstantBAR(metaclass=ConstantMetaBAR):
            pass

        with self.assertRaises(ConstantError):

            class ConstantFOOBAR(ConstantFOO, ConstantBAR):
                pass

if __name__ == "__main__":
    unittest.main()
