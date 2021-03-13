import unittest
import os
import sys

class OelintParserTest(unittest.TestCase):

    RECIPE = os.path.join(os.path.dirname(__file__), "test-recipe_1.0.bb")

    def setUp(self):
        sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/../"))

    def test_stash(self):
        from oelint_parser.cls_stash import Stash
        self.__stash = Stash()
        _stash = self.__stash.AddFile(OelintParserTest.RECIPE)
        self.assertTrue(_stash, msg="Stash has no items")

    def test_var(self):
        from oelint_parser.cls_item import Variable
        from oelint_parser.helper_files import expand_term
        from oelint_parser.cls_stash import Stash

        self.__stash = Stash()
        self.__stash.AddFile(OelintParserTest.RECIPE)

        _stash = self.__stash.GetItemsFor(classifier=Variable.CLASSIFIER, 
                                          attribute=Variable.ATTR_VAR, 
                                          attributeValue="LICENSE")
        self.assertTrue(_stash, msg="Stash has no items")
        for x in _stash:
            self.assertEqual(x.VarValue, '"BSD-2-Clause"')
            self.assertEqual(x.VarValueStripped, 'BSD-2-Clause')
            self.assertEqual(x.VarName, 'LICENSE')
            self.assertEqual(x.Raw, 'LICENSE = "BSD-2-Clause"\n')
            self.assertEqual(x.RawVarName, 'LICENSE')
            self.assertEqual(x.get_items(), ["BSD-2-Clause"])
            self.assertEqual(x.PkgSpec, [])
            self.assertEqual(x.SubItem, "")
            self.assertEqual(x.SubItems, [])
            self.assertEqual(x.VarOp, " = ")
            self.assertEqual(x.Flag, "")
            self.assertEqual(x.GetClassOverride(), "")

    def test_include(self):
        from oelint_parser.cls_item import Include
        from oelint_parser.helper_files import expand_term
        from oelint_parser.cls_stash import Stash

        self.__stash = Stash()
        self.__stash.AddFile(OelintParserTest.RECIPE)

        _stash = self.__stash.GetItemsFor(classifier=Include.CLASSIFIER)

        self.assertTrue(_stash, msg="Stash has no items")
        for x in _stash:
            self.assertEqual(x.Raw, "require another_file.inc\n")
            self.assertEqual(x.IncName, "another_file.inc")
            self.assertEqual(x.Statement, "require")

    def test_include(self):
        from oelint_parser.cls_item import Include
        from oelint_parser.helper_files import expand_term
        from oelint_parser.cls_stash import Stash

        self.__stash = Stash()
        self.__stash.AddFile(OelintParserTest.RECIPE)

        _stash = self.__stash.GetItemsFor(classifier=Include.CLASSIFIER)

        self.assertTrue(_stash, msg="Stash has no items")
        for x in _stash:
            self.assertEqual(x.Raw, "require another_file.inc\n")
            self.assertEqual(x.IncName, "another_file.inc")
            self.assertEqual(x.Statement, "require")
    
    def test_export(self):
        from oelint_parser.cls_item import Export
        from oelint_parser.helper_files import expand_term
        from oelint_parser.cls_stash import Stash

        self.__stash = Stash()
        self.__stash.AddFile(OelintParserTest.RECIPE)

        _stash = self.__stash.GetItemsFor(classifier=Export.CLASSIFIER)

        self.assertTrue(_stash, msg="Stash has no items")

        _withval = [x for x in _stash if x.Value]
        _woval = [x for x in _stash if not x.Value]
        self.assertTrue(_withval, msg="One item with value exists")
        self.assertTrue(_woval, msg="One item without value exists")
        
        self.assertEqual(_withval[0].Name, "lib")
        self.assertEqual(_withval[0].Value, "${bindir}/foo")

        self.assertEqual(_woval[0].Name, "PYTHON_ABI")
        self.assertEqual(_woval[0].Value, "")

    def test_taskassignment(self):
        from oelint_parser.cls_item import TaskAssignment
        from oelint_parser.helper_files import expand_term
        from oelint_parser.cls_stash import Stash

        self.__stash = Stash()
        self.__stash.AddFile(OelintParserTest.RECIPE)

        _stash = self.__stash.GetItemsFor(classifier=TaskAssignment.CLASSIFIER)

        self.assertTrue(_stash, msg="Stash has no items")
        for x in _stash:
            self.assertEqual(x.Raw, 'do_configure[noexec] = "1"\n')
            self.assertEqual(x.FuncName, "do_configure")
            self.assertEqual(x.VarValue, '"1"')
            self.assertEqual(x.VarName, "noexec")

    def test_pythonblock(self):
        from oelint_parser.cls_item import PythonBlock
        from oelint_parser.helper_files import expand_term
        from oelint_parser.cls_stash import Stash

        self.__stash = Stash()
        self.__stash.AddFile(OelintParserTest.RECIPE)

        _stash = self.__stash.GetItemsFor(classifier=PythonBlock.CLASSIFIER)

        self.assertTrue(_stash, msg="Stash has no items")
        for x in _stash:
            self.assertEqual(x.FuncName, "example_function")

    def test_taskadd(self):
        from oelint_parser.cls_item import TaskAdd
        from oelint_parser.helper_files import expand_term
        from oelint_parser.cls_stash import Stash

        self.__stash = Stash()
        self.__stash.AddFile(OelintParserTest.RECIPE)

        _stash = self.__stash.GetItemsFor(classifier=TaskAdd.CLASSIFIER)

        self.assertTrue(_stash, msg="Stash has no items")
        for x in _stash:
            self.assertEqual(x.FuncName, "do_example")
            self.assertEqual(x.After, ["do_foo"])
            self.assertEqual(x.Before, ["do_bar"])

    def test_function(self):
        from oelint_parser.cls_item import Function
        from oelint_parser.helper_files import expand_term
        from oelint_parser.cls_stash import Stash

        self.__stash = Stash()
        self.__stash.AddFile(OelintParserTest.RECIPE)

        _stash = self.__stash.GetItemsFor(classifier=Function.CLASSIFIER)

        self.assertTrue(_stash, msg="Stash has no items")
        self.assertTrue(any([x for x in _stash if "append" in x.SubItems]))
        self.assertTrue(any([x for x in _stash if "append" not in x.SubItems]))

        x = [x for x in _stash if "append" not in x.SubItems][0]
        self.assertEqual(x.IsPython, False)
        self.assertEqual(x.IsFakeroot, False)
        self.assertEqual(x.FuncName, "do_example")
        self.assertIn('bbwarn "This is an example warning"', x.FuncBody)
        self.assertEqual(x.IsAppend(), False)
        self.assertEqual(x.FuncBodyStripped, 'bbwarn "This is an example warning"')
        self.assertEqual(x.GetMachineEntry(), "")

        x = [x for x in _stash if "append" in x.SubItems][0]
        self.assertEqual(x.IsPython, True)
        self.assertEqual(x.IsFakeroot, True)
        self.assertEqual(x.FuncName, "do_something")
        self.assertIn('bb.warn("This is another example warning")', x.FuncBody)
        self.assertEqual(x.IsAppend(), True)
        self.assertEqual(x.FuncBodyStripped, 'bb.warn("This is another example warning")')
        self.assertEqual(x.GetMachineEntry(), "")

    def test_varflag(self):
        from oelint_parser.cls_item import Variable
        from oelint_parser.helper_files import expand_term
        from oelint_parser.cls_stash import Stash

        self.__stash = Stash()
        self.__stash.AddFile(OelintParserTest.RECIPE)

        _stash = self.__stash.GetItemsFor(classifier=Variable.CLASSIFIER, 
                                          attribute=Variable.ATTR_VAR, 
                                          attributeValue="PACKAGECONFIG")
        self.assertTrue(_stash, msg="Stash has no items")
        for x in _stash:
            self.assertEqual(x.VarName, "PACKAGECONFIG")
            self.assertEqual(x.Flag, "abc")
            self.assertEqual(x.RawVarName, "PACKAGECONFIG[abc]")

    def test_multiline(self):
        from oelint_parser.cls_item import Variable
        from oelint_parser.helper_files import expand_term
        from oelint_parser.cls_stash import Stash

        self.__stash = Stash()
        self.__stash.AddFile(OelintParserTest.RECIPE)

        _stash = self.__stash.GetItemsFor(classifier=Variable.CLASSIFIER, 
                                          attribute=Variable.ATTR_VAR, 
                                          attributeValue="SOMELIST")
        self.assertTrue(_stash, msg="Stash has no items")
        for x in _stash:
            self.assertEqual(x.VarName, "SOMELIST")
            self.assertEqual(x.get_items(), ["a", "b", "c"])

    def test_expand(self):
        from oelint_parser.cls_item import Variable
        from oelint_parser.helper_files import expand_term
        from oelint_parser.cls_stash import Stash

        self.__stash = Stash()
        self.__stash.AddFile(OelintParserTest.RECIPE)

        _stash = self.__stash.GetItemsFor(classifier=Variable.CLASSIFIER, 
                                          attribute=Variable.ATTR_VAR, 
                                          attributeValue="SOMEOTHERVAR")
        self.assertTrue(_stash, msg="Stash has no items")
        for x in _stash:
            self.assertEqual(x.VarName, "SOMEOTHERVAR")
            self.assertEqual(expand_term(self.__stash, 
                                OelintParserTest.RECIPE,
                                x.VarValueStripped), "source/SOMEMORE")
            self.assertNotEqual(x.VarValueStripped, "source/SOMEMORE")

    def test_inlinecodeblock(self):
        from oelint_parser.cls_item import Variable
        from oelint_parser.helper_files import expand_term
        from oelint_parser.cls_stash import Stash

        self.__stash = Stash()
        self.__stash.AddFile(OelintParserTest.RECIPE)

        _stash = self.__stash.GetItemsFor(classifier=Variable.CLASSIFIER, 
                                          attribute=Variable.ATTR_VAR, 
                                          attributeValue="INLINECODEBLOCK")
        self.assertTrue(_stash, msg="Stash has no items")
        for x in _stash:
            self.assertEqual(x.VarName, "INLINECODEBLOCK")
            self.assertEqual(x.VarValueStripped, "systemd-systemctl-native")
            self.assertNotEqual(x.Raw, x.RealRaw)

    def test_lineattributerw(self):
        from oelint_parser.cls_item import Variable
        from oelint_parser.helper_files import expand_term
        from oelint_parser.cls_stash import Stash

        self.__stash = Stash()
        self.__stash.AddFile(OelintParserTest.RECIPE)

        _stash = self.__stash.GetItemsFor(classifier=Variable.CLASSIFIER)
        self.assertTrue(_stash, msg="Stash has no items")
        try:
            _stash[0].Line = 10000
        except Exception as e:
            self.fail("Setting Line attribute shouldn't raise an exception")

    def test_multiline_no_ml(self):
        from oelint_parser.cls_item import Variable
        from oelint_parser.cls_stash import Stash

        self.__stash = Stash()
        self.__stash.AddFile(OelintParserTest.RECIPE)

        _stash = self.__stash.GetItemsFor(classifier=Variable.CLASSIFIER,
                                          attribute=Variable.ATTR_VAR, 
                                          attributeValue="UPSTREAM_CHECK_REGEX")
        self.assertTrue(_stash, msg="Stash has no items")
        self.assertFalse(_stash[0].IsMultiLine(), msg="UPSTREAM_CHECK_REGEX is no multiline")

    def test_multiline_ml(self):
        from oelint_parser.cls_item import Variable
        from oelint_parser.cls_stash import Stash

        self.__stash = Stash()
        self.__stash.AddFile(OelintParserTest.RECIPE)

        _stash = self.__stash.GetItemsFor(classifier=Variable.CLASSIFIER,
                                          attribute=Variable.ATTR_VAR, 
                                          attributeValue="SOMELIST")
        self.assertTrue(_stash, msg="Stash has no items")
        self.assertTrue(_stash[0].IsMultiLine(), msg="SOMELIST is a multiline")

    def test_class_target(self):
        from oelint_parser.cls_item import Variable
        from oelint_parser.helper_files import expand_term
        from oelint_parser.cls_stash import Stash

        self.__stash = Stash()
        self.__stash.AddFile(OelintParserTest.RECIPE)

        _stash = self.__stash.GetItemsFor(classifier=Variable.CLASSIFIER, 
                                          attribute=Variable.ATTR_VAR, 
                                          attributeValue="TARGETVAR")
        self.assertTrue(_stash, msg="Stash has no items")
        for x in _stash:
            self.assertEqual(x.VarValueStripped, 'foo')
            self.assertEqual(x.VarName, 'TARGETVAR')
            self.assertEqual(x.GetClassOverride(), 'class-target')

    def test_class_cross(self):
        from oelint_parser.cls_item import Variable
        from oelint_parser.helper_files import expand_term
        from oelint_parser.cls_stash import Stash

        self.__stash = Stash()
        self.__stash.AddFile(OelintParserTest.RECIPE)

        _stash = self.__stash.GetItemsFor(classifier=Variable.CLASSIFIER, 
                                          attribute=Variable.ATTR_VAR, 
                                          attributeValue="CROSSVAR")
        self.assertTrue(_stash, msg="Stash has no items")
        for x in _stash:
            self.assertEqual(x.VarValueStripped, 'foo')
            self.assertEqual(x.VarName, 'CROSSVAR')
            self.assertEqual(x.GetClassOverride(), 'class-cross')

    def test_class_native(self):
        from oelint_parser.cls_item import Variable
        from oelint_parser.helper_files import expand_term
        from oelint_parser.cls_stash import Stash

        self.__stash = Stash()
        self.__stash.AddFile(OelintParserTest.RECIPE)

        _stash = self.__stash.GetItemsFor(classifier=Variable.CLASSIFIER, 
                                          attribute=Variable.ATTR_VAR, 
                                          attributeValue="NATIVEVAR")
        self.assertTrue(_stash, msg="Stash has no items")
        for x in _stash:
            self.assertEqual(x.VarValueStripped, 'foo')
            self.assertEqual(x.VarName, 'NATIVEVAR')
            self.assertEqual(x.GetClassOverride(), 'class-native')

    def test_class_nativesdk(self):
        from oelint_parser.cls_item import Variable
        from oelint_parser.helper_files import expand_term
        from oelint_parser.cls_stash import Stash

        self.__stash = Stash()
        self.__stash.AddFile(OelintParserTest.RECIPE)

        _stash = self.__stash.GetItemsFor(classifier=Variable.CLASSIFIER, 
                                          attribute=Variable.ATTR_VAR, 
                                          attributeValue="SDKVAR")
        self.assertTrue(_stash, msg="Stash has no items")
        for x in _stash:
            self.assertEqual(x.VarValueStripped, 'foo')
            self.assertEqual(x.VarName, 'SDKVAR')
            self.assertEqual(x.GetClassOverride(), 'class-nativesdk')

if __name__ == "__main__": 
    unittest.main()