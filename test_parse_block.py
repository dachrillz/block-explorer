import unittest
import modules.models as m

REFERENCE_BLOCK = {
    "hash":"0000000000000bae09a7a393a8acded75aa67e46cb81f7acaa5ad94f9eacd103",
    "ver":1,
    "prev_block":"00000000000007d0f98d9edca880a6c124e25095712df8952e0439ac7409738a",
    "mrkl_root":"935aa0ed2e29a4b81e0c995c39e06995ecce7ddbebb26ed32d550a72e8200bf5",
    "time":1322131230,
    "bits":437129626,
    "nonce":2964215930,
    "n_tx":22,
    "size":9195,
    "block_index":818044,
    "main_chain":True,
    "height":154595,
    "received_time":1322131301,
    "relayed_by":"108.60.208.156",
    "tx":["--Array of Transactions--"] 
    }

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)
    
    def test_parse_compact_unsigned_int(self):
        # First
        _input = "fd0302"
        _expected = 515
        model = m.CompactSizeUnsignedInteger(_input, None, None)
        value = model.get_value()
        self.assertEqual(value, _expected)

        _input = "fe703a0f00"
        _expected = 998000

        model = m.CompactSizeUnsignedInteger(_input, None, None)
        value = model.get_value()
        self.assertEqual(value, _expected)

        _input = "6a"
        _expected = 106
        model = m.CompactSizeUnsignedInteger(_input, None, None)
        value = model.get_value()
        self.assertEqual(value, _expected)


if __name__ == '__main__':
    unittest.main()