# -*- encoding: utf-8 -*-
import unittest

from urbanus.pipelines import _convert_price_to_soles


class TestPipeline(unittest.TestCase):
    def test_coverting_price_to_soles(self):
        result = _convert_price_to_soles("US$ 500")
        self.assertEqual(1600.0, result)

        result = _convert_price_to_soles("US$ 1,500")
        self.assertEqual(4800.0, result)

        result = _convert_price_to_soles("Consultar")
        self.assertEqual(0, result)

        result = _convert_price_to_soles("S/. 1,200")
        self.assertEqual(1200, result)
