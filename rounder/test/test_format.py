"""
Tests for extended formatting functionality.
"""

import decimal
import fractions
import unittest


from rounder import format


class TestFormat(unittest.TestCase):
    def test_format_fraction(self):
        self.assertEqual(format(fractions.Fraction(3, 7), ".3f"), "0.429")
        self.assertEqual(format(fractions.Fraction(3, 7), ".4f"), "0.4286")
        self.assertEqual(format(fractions.Fraction(3, 7), ".5f"), "0.42857")

    def test_format_rounding_mode(self):
        cases = [
            ("-0.4277", ".3Mf", "-0.428"),
            ("-0.4277", ".3Pf", "-0.427"),
            ("-0.4277", ".3Zf", "-0.427"),
            ("-0.4277", ".3Af", "-0.428"),
            ("-0.4277", ".3Ef", "-0.428"),
            ("-0.4277", ".3Of", "-0.427"),
            ("-0.4277", ".3mf", "-0.428"),
            ("-0.4277", ".3pf", "-0.428"),
            ("-0.4277", ".3zf", "-0.428"),
            ("-0.4277", ".3af", "-0.428"),
            ("-0.4277", ".3ef", "-0.428"),
            ("-0.4277", ".3of", "-0.428"),
            ("+0.4275", ".3Mf", "0.427"),
            ("+0.4275", ".3Pf", "0.428"),
            ("+0.4275", ".3Zf", "0.427"),
            ("+0.4275", ".3Af", "0.428"),
            ("+0.4275", ".3Ef", "0.428"),
            ("+0.4275", ".3Of", "0.427"),
            ("+0.4275", ".3mf", "0.427"),
            ("+0.4275", ".3pf", "0.428"),
            ("+0.4275", ".3zf", "0.427"),
            ("+0.4275", ".3af", "0.428"),
            ("+0.4275", ".3ef", "0.428"),
            ("+0.4275", ".3of", "0.427"),
            ("+0.4277", ".3Mf", "0.427"),
            ("+0.4277", ".3Pf", "0.428"),
            ("+0.4277", ".3Zf", "0.427"),
            ("+0.4277", ".3Af", "0.428"),
            ("+0.4277", ".3Ef", "0.428"),
            ("+0.4277", ".3Of", "0.427"),
            ("+0.4277", ".3mf", "0.428"),
            ("+0.4277", ".3pf", "0.428"),
            ("+0.4277", ".3zf", "0.428"),
            ("+0.4277", ".3af", "0.428"),
            ("+0.4277", ".3ef", "0.428"),
            ("+0.4277", ".3of", "0.428"),
            ("+0.4285", ".3Mf", "0.428"),
            ("+0.4285", ".3Pf", "0.429"),
            ("+0.4285", ".3Zf", "0.428"),
            ("+0.4285", ".3Af", "0.429"),
            ("+0.4285", ".3Ef", "0.428"),
            ("+0.4285", ".3Of", "0.429"),
            ("+0.4285", ".3mf", "0.428"),
            ("+0.4285", ".3pf", "0.429"),
            ("+0.4285", ".3zf", "0.428"),
            ("+0.4285", ".3af", "0.429"),
            ("+0.4285", ".3ef", "0.428"),
            ("+0.4285", ".3of", "0.429"),
            ("+0.4287", ".3Mf", "0.428"),
            ("+0.4287", ".3Pf", "0.429"),
            ("+0.4287", ".3Zf", "0.428"),
            ("+0.4287", ".3Af", "0.429"),
            ("+0.4287", ".3Ef", "0.428"),
            ("+0.4287", ".3Of", "0.429"),
            ("+0.4287", ".3mf", "0.429"),
            ("+0.4287", ".3pf", "0.429"),
            ("+0.4287", ".3zf", "0.429"),
            ("+0.4287", ".3af", "0.429"),
            ("+0.4287", ".3ef", "0.429"),
            ("+0.4287", ".3of", "0.429"),

            ("+0.4200", ".3Rf", "0.420"),
            ("+0.4210", ".3Rf", "0.421"),
            ("+0.4220", ".3Rf", "0.422"),
            ("+0.4230", ".3Rf", "0.423"),
            ("+0.4240", ".3Rf", "0.424"),
            ("+0.4250", ".3Rf", "0.425"),
            ("+0.4260", ".3Rf", "0.426"),
            ("+0.4270", ".3Rf", "0.427"),
            ("+0.4280", ".3Rf", "0.428"),
            ("+0.4290", ".3Rf", "0.429"),

            ("+0.4202", ".3Rf", "0.421"),
            ("+0.4212", ".3Rf", "0.421"),
            ("+0.4222", ".3Rf", "0.422"),
            ("+0.4232", ".3Rf", "0.423"),
            ("+0.4242", ".3Rf", "0.424"),
            ("+0.4252", ".3Rf", "0.426"),
            ("+0.4262", ".3Rf", "0.426"),
            ("+0.4272", ".3Rf", "0.427"),
            ("+0.4282", ".3Rf", "0.428"),
            ("+0.4292", ".3Rf", "0.429"),

            ("+0.4208", ".3Rf", "0.421"),
            ("+0.4218", ".3Rf", "0.421"),
            ("+0.4228", ".3Rf", "0.422"),
            ("+0.4238", ".3Rf", "0.423"),
            ("+0.4248", ".3Rf", "0.424"),
            ("+0.4258", ".3Rf", "0.426"),
            ("+0.4268", ".3Rf", "0.426"),
            ("+0.4278", ".3Rf", "0.427"),
            ("+0.4288", ".3Rf", "0.428"),
            ("+0.4298", ".3Rf", "0.429"),
        ]
        for case in cases:
            value, pattern, expected_result = case
            with self.subTest(case=case):
                value = decimal.Decimal(value)
                actual_result = format(value, pattern)
                self.assertEqual(actual_result, expected_result)
