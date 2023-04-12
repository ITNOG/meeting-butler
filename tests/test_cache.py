import os
import unittest

from meeting_butler.cache import Cache


class TestCache(unittest.TestCase):
    def setUp(self):
        self.cache = Cache(reset=True)

    def tearDown(self):
        self.cache.close()
        os.unlink(self.cache.filename)

    def test_insert(self):
        self.cache["1"] = 2
        with self.assertRaises(TypeError):
            self.cache[1] = 2
        with self.assertRaises(TypeError):
            self.cache[{}] = 2
        with self.assertRaises(TypeError):
            self.cache[[]] = 2

    def test_get(self):
        self.cache["1"] = {"2": 3}
        self.assertEqual(self.cache["1"], {"2": 3})
        with self.assertRaises(KeyError):
            self.cache["->WRONG<-"]

        self.assertListEqual(self.cache.keys(), ["1"])
        self.assertListEqual(self.cache.values(), [{"2": 3}])
        self.assertListEqual(self.cache.items(), [("1", {"2": 3})])

    def test_delete(self):
        self.cache["1"] = 2
        del self.cache["1"]
        with self.assertRaises(KeyError):
            del self.cache["->WRONG<-"]
