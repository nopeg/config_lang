import unittest
from main import parse_config


class TestParseConfig(unittest.TestCase):
    def test_string_values(self):
        config_text = """
        app_name := [[MyApp]];
        version := [[1.0.3]];
        """
        config = parse_config(config_text)
        self.assertEqual(config['app_name'], 'MyApp')
        self.assertEqual(config['version'], '1.0.3')

    def test_boolean_values(self):
        config_text = """
        debug_mode := true;
        maintenance := false;
        """
        config = parse_config(config_text)
        self.assertTrue(config['debug_mode'])
        self.assertFalse(config['maintenance'])

    def test_numeric_values(self):
        config_text = """
        max_connections := 15;
        timeout := ^(10 5 +);
        """
        config = parse_config(config_text)
        self.assertEqual(config['max_connections'], 15)
        self.assertEqual(config['timeout'], 15)
    def test_empty_values(self):
        config_text = """
        app_name := [[]];
        """
        config = parse_config(config_text)
        self.assertEqual(config['app_name'], '')

    def test_multi_block_parsing(self):
        config_text = """
        {
            app_name := [[MyApp]];
            version := [[1.0.3]];
            debug_mode := true;
            max_connections := ^(10 5 +);
        }

        {
            database := [[app_db]];
            user := [[admin]];
            password := [[secret]];
        }
        """
        config = parse_config(config_text)
        self.assertEqual(config['app_name'], 'MyApp')
        self.assertEqual(config['version'], '1.0.3')
        self.assertTrue(config['debug_mode'])
        self.assertEqual(config['max_connections'], 15)
        self.assertEqual(config['database'], 'app_db')
        self.assertEqual(config['user'], 'admin')
        self.assertEqual(config['password'], 'secret')

    def test_functions_max_sqrt(self):
        config_text = """
        sum_value := ^(5 10 +);
        ord_value := ^(1 ord());
        """
        config = parse_config(config_text)
        self.assertEqual(config['sum_value'], 15)
        self.assertEqual(config['ord_value'], 49)


if __name__ == "__main__":
    unittest.main()
