import unittest


from constant import Constant, ConstantError


class TestConstant(unittest.TestCase):

    def test_constant(self):
        with self.subTest(case="consant write"):
            with self.assertRaises(ConstantError):
                Constant.FOO = "new_foo"
            with self.assertRaises(ConstantError):
                Constant.BAR = "new_bar"
            with self.assertRaises(ConstantError):
                Constant.BAZ = "new_baz"

    def test_standard_constant(self):
        # Define standard constant class
        class StandardConstant(Constant):
            FOO = "foo"
            BAR = "bar"
            BAZ = "baz"

        with self.subTest(case="constant read"):
            self.assertEqual(StandardConstant.FOO, "foo")
            self.assertEqual(StandardConstant.BAR, "bar")
            self.assertEqual(StandardConstant.BAZ, "baz")

        with self.subTest(case="consant overwrite"):
            with self.assertRaises(ConstantError):
                StandardConstant.FOO = "new_foo"
            with self.assertRaises(ConstantError):
                StandardConstant.BAR = "new_bar"
            with self.assertRaises(ConstantError):
                StandardConstant.BAZ = "new_baz"

        with self.subTest(case="unsettable attribute write"):
            with self.assertRaises(ConstantError):
                StandardConstant.FIZZ = "fizz"
            with self.assertRaises(ConstantError):
                StandardConstant.BUZZ = "buzz"

        with self.subTest(case="instantiation"):
            with self.assertRaises(ConstantError):
                StandardConstant()

    def test_extend_constant(self):
        # Define base constant class
        class BaseConstant(Constant):
            FOO = "foo"
            BAR = "bar"
            BAZ = "baz"

        class ExtendConstant(BaseConstant):
            FIZZ = "fizz"
            BUZZ = "buzz"

        with self.subTest(case="constant read"):
            self.assertEqual(ExtendConstant.FOO, "foo")
            self.assertEqual(ExtendConstant.BAR, "bar")
            self.assertEqual(ExtendConstant.BAZ, "baz")

            self.assertEqual(ExtendConstant.FIZZ, "fizz")
            self.assertEqual(ExtendConstant.BUZZ, "buzz")

    def test_multi_extend_constant(self):

        class ConstantFOO(Constant):
            FOO = "foo"

        class ConstantBAR(Constant):
            BAR = "bar"

        class ConstantFOOBAR(ConstantFOO, ConstantBAR):
            FOOBAR = "foobar"

        with self.subTest(case="constant read"):
            self.assertEqual(ConstantFOOBAR.FOO, "foo")
            self.assertEqual(ConstantFOOBAR.BAR, "bar")
            self.assertEqual(ConstantFOOBAR.FOOBAR, "foobar")

    def test_collision_constant(self):

        class ConstantFOOX(Constant):
            FOO = "foox"

        class ConstantFOOY(Constant):
            FOO = "fooy"

        with self.assertRaises(ConstantError):
            class ConstantFOOXY(ConstantFOOX, ConstantFOOY):
                pass

    def test_rebind_constant(self):

        class ConstantFOOX(Constant):
            FOO = "foox"

        with self.assertRaises(ConstantError):
            class ConstantFOOY(ConstantFOOX):
                FOO = "fooy"


if __name__ == "__main__":
    unittest.main()
