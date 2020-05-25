import unittest

from renameit.handlers import RegexFileNameHandler


class TestRegexFileNameHandler(unittest.TestCase):
    def setUp(self):
        self.regex_config = {
            "regex_pattern": r"^(?P<group1>.*)_(?P<group2>.*).txt$",
            "replace_pattern": "{group1}_{group2}.txt",
            "groups": {
                "group1": {"test": "FirstPart"},
                "group2": {"file": "SecondPart"},
            },
        }
        self.handler = RegexFileNameHandler(regex_config=self.regex_config)

    def test_rename_file_cs(self):
        self.handler.case_sensitive = True

        self.assertEquals(
            self.handler.process("test_file.txt"),
            "FirstPart_SecondPart.txt",
            "File should be renamed.",
        )

        self.assertNotEquals(
            self.handler.process("Test_File.txt"),
            "FirstPart_SecondPart.txt",
            "File should not be renamed.",
        )

        self.assertEquals(
            self.handler.process("Test_File.txt"),
            "Test_File.txt",
            "File name should remain the same.",
        )

    def test_rename_file_ci(self):
        self.handler.case_sensitive = False

        self.assertEquals(
            self.handler.process("TeSt_fIlE.txt"),
            "FirstPart_SecondPart.txt",
            "File should be renamed.",
        )

        self.assertEquals(
            self.handler.process("test_file.txt"),
            "FirstPart_SecondPart.txt",
            "File should be renamed.",
        )
