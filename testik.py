import unittest
import yaml
from Chto import fix_name, process_value, process_dict, process_list, process_yaml_string

class TestConfigConverter(unittest.TestCase):

    def test_fix_name(self):
        """
        Тестирование функции fix_name.
        """
        # Проверка преобразования маленьких букв в большие
        self.assertEqual(fix_name("aa11"), "AAONEONE")
        with self.assertRaises(ValueError):
            fix_name("!@#")
            
    def test_process_yaml_string(self):
        """
        Тестирование функции process_yaml_string.
        """
        # Проверка YAML-строки
        yaml_string = """
key1: value1
key2:
  subkey1: subvalue1
  subkey2: subvalue2
key3:
  - item1: ASD
  - item2
"""
        expected_output = (
            "var KEYONE [[value1]]\n"
            "var KEYTWO {\n"
            "var SUBKEYONE [[subvalue1]]\n"
            "var SUBKEYTWO [[subvalue2]]\n"
            "}\n"
            "var KEYTHREE <[ ITEMONE: [[ASD]], ITEMTWO ]>"
        )
        self.assertEqual(process_yaml_string(yaml_string), expected_output)

if __name__ == "__main__":
    unittest.main()
