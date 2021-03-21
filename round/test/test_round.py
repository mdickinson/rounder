"""
Tests for functions in the 'round' module.
"""

import decimal
import fractions
import math
import unittest

from round import (
    # Midpoint rounding methods
    round_ties_to_away,
    round_ties_to_zero,
    round_ties_to_plus,
    round_ties_to_minus,
    round_ties_to_even,
    round_ties_to_odd,
    # Directed rounding methods
    round_to_away,
    round_to_zero,
    round_to_plus,
    round_to_minus,
    round_to_even,
    round_to_odd,
    # round to significant figures
    round_to_figures,
    # rounding modes
    TIES_TO_EVEN,
    TIES_TO_ODD,
    TIES_TO_AWAY,
    TIES_TO_ZERO,
    TIES_TO_PLUS,
    TIES_TO_MINUS,
)


#: A selection of IEEE 754 binary64 floating-point values used in a wide
#: variety of tests.
ALL_POSITIVE_TEST_VALUES = [
    *[0.25 * n for n in range(100)],  # quarter integers from 0.0 to 24.75
    4503599627370495.5,  # largest representable non-integral half integer
    float.fromhex("0x0.0000000000001p-1022"),  # smallest +ve subnormal
    float.fromhex("0x0.fffffffffffffp-1022"),  # largest +ve subnormal
    float.fromhex("0x1.fffffffffffffp-2"),  # largest value < 0.5
    float.fromhex("0x1.0000000000001p-1"),  # largest value > 0.5
    float.fromhex("0x1.fffffffffffffp+1023"),  # largest finite value
]

ALL_TEST_VALUES = [
    signed_value
    for value in ALL_POSITIVE_TEST_VALUES
    for signed_value in [-value, value]
]


#: Pairs (e, x) where x is a float and e is the decade of that float;
#: that is, 10**e <= abs(x) < 10**(e+1)
TEN = fractions.Fraction(10)

DECADE_STARTS = []
for e in range(-324, 309):
    try:
        x = float(TEN ** e)
    except OverflowError:
        x = math.inf
    if x < TEN ** e:
        x = math.nextafter(x, math.inf)

    assert TEN ** e <= x < TEN ** (e + 1)
    assert not (TEN ** e <= math.nextafter(x, 0.0) < TEN ** (e + 1))
    DECADE_STARTS.append((e, x))

DECADE_ENDS = []
for e in range(-324, 309):
    try:
        x = float(TEN ** (e + 1))
    except OverflowError:
        x = math.inf
    if x >= TEN ** (e + 1):
        x = math.nextafter(x, 0.0)

    assert TEN ** e <= x < TEN ** (e + 1)
    assert not (TEN ** e <= math.nextafter(x, math.inf) < TEN ** (e + 1))
    DECADE_ENDS.append((e, x))

DECADE_TEST_VALUES = DECADE_STARTS + DECADE_ENDS


#: Various subsets of the rounding functions
MIDPOINT_ROUNDING_FUNCTIONS = [
    round_ties_to_even,
    round_ties_to_odd,
    round_ties_to_away,
    round_ties_to_zero,
    round_ties_to_plus,
    round_ties_to_minus,
]

DIRECTED_ROUNDING_FUNCTIONS = [
    round_to_even,
    round_to_odd,
    round_to_away,
    round_to_zero,
    round_to_plus,
    round_to_minus,
]

ALL_ROUNDING_FUNCTIONS = MIDPOINT_ROUNDING_FUNCTIONS + DIRECTED_ROUNDING_FUNCTIONS


#: One half, as a fraction constant.
ONE_HALF = fractions.Fraction("1/2")


def sign_bit(x):
    """
    Sign bit of a float: True if negative, False if positive.
    """
    return math.copysign(1.0, x) < 0


class TestRound(unittest.TestCase):
    def test_round_ties_to_away_quarters(self):
        test_cases = [
            (-2.0, -2),
            (-1.75, -2),
            (-1.5, -2),
            (-1.25, -1),
            (-1.0, -1),
            (-0.75, -1),
            (-0.5, -1),
            (-0.25, 0),
            (-0.0, 0),
            (0.0, 0),
            (0.25, 0),
            (0.5, 1),
            (0.75, 1),
            (1.0, 1),
            (1.25, 1),
            (1.5, 2),
            (1.75, 2),
            (2.0, 2),
        ]
        for value, expected_result in test_cases:
            with self.subTest(value=value):
                actual_result = round_ties_to_away(value)
                self.assertIntsIdentical(actual_result, expected_result)

    def test_round_ties_to_zero_quarters(self):
        test_cases = [
            (-2.0, -2),
            (-1.75, -2),
            (-1.5, -1),
            (-1.25, -1),
            (-1.0, -1),
            (-0.75, -1),
            (-0.5, 0),
            (-0.25, 0),
            (-0.0, 0),
            (0.0, 0),
            (0.25, 0),
            (0.5, 0),
            (0.75, 1),
            (1.0, 1),
            (1.25, 1),
            (1.5, 1),
            (1.75, 2),
            (2.0, 2),
        ]
        for value, expected_result in test_cases:
            with self.subTest(value=value):
                actual_result = round_ties_to_zero(value)
                self.assertIntsIdentical(actual_result, expected_result)

    def test_round_ties_to_even_quarters(self):
        test_cases = [
            (-2.0, -2),
            (-1.75, -2),
            (-1.5, -2),
            (-1.25, -1),
            (-1.0, -1),
            (-0.75, -1),
            (-0.5, 0),
            (-0.25, 0),
            (-0.0, 0),
            (0.0, 0),
            (0.25, 0),
            (0.5, 0),
            (0.75, 1),
            (1.0, 1),
            (1.25, 1),
            (1.5, 2),
            (1.75, 2),
            (2.0, 2),
        ]
        for value, expected_result in test_cases:
            with self.subTest(value=value):
                actual_result = round_ties_to_even(value)
                self.assertIntsIdentical(actual_result, expected_result)

    def test_round_ties_to_odd_quarters(self):
        test_cases = [
            (-2.0, -2),
            (-1.75, -2),
            (-1.5, -1),
            (-1.25, -1),
            (-1.0, -1),
            (-0.75, -1),
            (-0.5, -1),
            (-0.25, 0),
            (-0.0, 0),
            (0.0, 0),
            (0.25, 0),
            (0.5, 1),
            (0.75, 1),
            (1.0, 1),
            (1.25, 1),
            (1.5, 1),
            (1.75, 2),
            (2.0, 2),
        ]
        for value, expected_result in test_cases:
            with self.subTest(value=value):
                actual_result = round_ties_to_odd(value)
                self.assertIntsIdentical(actual_result, expected_result)

    def test_round_ties_to_plus_quarters(self):
        test_cases = [
            (-2.0, -2),
            (-1.75, -2),
            (-1.5, -1),
            (-1.25, -1),
            (-1.0, -1),
            (-0.75, -1),
            (-0.5, 0),
            (-0.25, 0),
            (-0.0, 0),
            (0.0, 0),
            (0.25, 0),
            (0.5, 1),
            (0.75, 1),
            (1.0, 1),
            (1.25, 1),
            (1.5, 2),
            (1.75, 2),
            (2.0, 2),
        ]
        for value, expected_result in test_cases:
            with self.subTest(value=value):
                actual_result = round_ties_to_plus(value)
                self.assertIntsIdentical(actual_result, expected_result)

    def test_round_ties_to_minus_quarters(self):
        test_cases = [
            (-2.0, -2),
            (-1.75, -2),
            (-1.5, -2),
            (-1.25, -1),
            (-1.0, -1),
            (-0.75, -1),
            (-0.5, -1),
            (-0.25, 0),
            (-0.0, 0),
            (0.0, 0),
            (0.25, 0),
            (0.5, 0),
            (0.75, 1),
            (1.0, 1),
            (1.25, 1),
            (1.5, 1),
            (1.75, 2),
            (2.0, 2),
        ]
        for value, expected_result in test_cases:
            with self.subTest(value=value):
                actual_result = round_ties_to_minus(value)
                self.assertIntsIdentical(actual_result, expected_result)

    def test_round_to_away_quarters(self):
        test_cases = [
            (-2.0, -2),
            (-1.75, -2),
            (-1.5, -2),
            (-1.25, -2),
            (-1.0, -1),
            (-0.75, -1),
            (-0.5, -1),
            (-0.25, -1),
            (-0.0, 0),
            (0.0, 0),
            (0.25, 1),
            (0.5, 1),
            (0.75, 1),
            (1.0, 1),
            (1.25, 2),
            (1.5, 2),
            (1.75, 2),
            (2.0, 2),
        ]
        for value, expected_result in test_cases:
            with self.subTest(value=value):
                actual_result = round_to_away(value)
                self.assertIntsIdentical(actual_result, expected_result)

    def test_round_to_zero_quarters(self):
        test_cases = [
            (-2.0, -2),
            (-1.75, -1),
            (-1.5, -1),
            (-1.25, -1),
            (-1.0, -1),
            (-0.75, 0),
            (-0.5, 0),
            (-0.25, 0),
            (-0.0, 0),
            (0.0, 0),
            (0.25, 0),
            (0.5, 0),
            (0.75, 0),
            (1.0, 1),
            (1.25, 1),
            (1.5, 1),
            (1.75, 1),
            (2.0, 2),
        ]
        for value, expected_result in test_cases:
            with self.subTest(value=value):
                actual_result = round_to_zero(value)
                self.assertIntsIdentical(actual_result, expected_result)

    def test_round_to_plus_quarters(self):
        test_cases = [
            (-2.0, -2),
            (-1.75, -1),
            (-1.5, -1),
            (-1.25, -1),
            (-1.0, -1),
            (-0.75, 0),
            (-0.5, 0),
            (-0.25, 0),
            (-0.0, 0),
            (0.0, 0),
            (0.25, 1),
            (0.5, 1),
            (0.75, 1),
            (1.0, 1),
            (1.25, 2),
            (1.5, 2),
            (1.75, 2),
            (2.0, 2),
        ]
        for value, expected_result in test_cases:
            with self.subTest(value=value):
                actual_result = round_to_plus(value)
                self.assertIntsIdentical(actual_result, expected_result)

    def test_round_to_minus_quarters(self):
        test_cases = [
            (-2.0, -2),
            (-1.75, -2),
            (-1.5, -2),
            (-1.25, -2),
            (-1.0, -1),
            (-0.75, -1),
            (-0.5, -1),
            (-0.25, -1),
            (-0.0, 0),
            (0.0, 0),
            (0.25, 0),
            (0.5, 0),
            (0.75, 0),
            (1.0, 1),
            (1.25, 1),
            (1.5, 1),
            (1.75, 1),
            (2.0, 2),
        ]
        for value, expected_result in test_cases:
            with self.subTest(value=value):
                actual_result = round_to_minus(value)
                self.assertIntsIdentical(actual_result, expected_result)

    def test_round_to_even_quarters(self):
        test_cases = [
            (-2.0, -2),
            (-1.75, -2),
            (-1.5, -2),
            (-1.25, -2),
            (-1.0, -1),
            (-0.75, 0),
            (-0.5, 0),
            (-0.25, 0),
            (-0.0, 0),
            (0.0, 0),
            (0.25, 0),
            (0.5, 0),
            (0.75, 0),
            (1.0, 1),
            (1.25, 2),
            (1.5, 2),
            (1.75, 2),
            (2.0, 2),
        ]
        for value, expected_result in test_cases:
            with self.subTest(value=value):
                actual_result = round_to_even(value)
                self.assertIntsIdentical(actual_result, expected_result)

    def test_round_to_odd_quarters(self):
        test_cases = [
            (-2.0, -2),
            (-1.75, -1),
            (-1.5, -1),
            (-1.25, -1),
            (-1.0, -1),
            (-0.75, -1),
            (-0.5, -1),
            (-0.25, -1),
            (-0.0, 0),
            (0.0, 0),
            (0.25, 1),
            (0.5, 1),
            (0.75, 1),
            (1.0, 1),
            (1.25, 1),
            (1.5, 1),
            (1.75, 1),
            (2.0, 2),
        ]
        for value, expected_result in test_cases:
            with self.subTest(value=value):
                actual_result = round_to_odd(value)
                self.assertIntsIdentical(actual_result, expected_result)

    def test_all_midpoint_rounding_modes_round_to_nearest(self):
        # Difference between rounded value and original value should always
        # at most 0.5 in absolute value.
        for round_function in MIDPOINT_ROUNDING_FUNCTIONS:
            for original_value in ALL_TEST_VALUES:
                rounded_value = round_function(original_value)
                diff = fractions.Fraction(rounded_value) - fractions.Fraction(
                    original_value
                )
                self.assertLessEqual(abs(diff), ONE_HALF)

    def test_all_rounding_modes_round_to_neighbour(self):
        # Difference between rounded value and original value should always
        # be strictly less than 1.0 in absolute value.
        for round_function in ALL_ROUNDING_FUNCTIONS:
            for original_value in ALL_TEST_VALUES:
                rounded_value = round_function(original_value)
                diff = fractions.Fraction(rounded_value) - fractions.Fraction(
                    original_value
                )
                self.assertLessEqual(abs(diff), 1)

    def test_infinities(self):
        for round_function in ALL_ROUNDING_FUNCTIONS:
            for infinity in [math.inf, -math.inf]:
                with self.assertRaises(ValueError):
                    round_function(infinity)

    def test_nan(self):
        for round_function in ALL_ROUNDING_FUNCTIONS:
            with self.assertRaises(ValueError):
                round_function(math.nan)

    def test_round_to_decimal_places(self):
        self.assertFloatsIdentical(round_ties_to_away(66.15, -2), 100.0)
        self.assertFloatsIdentical(round_ties_to_away(66.15, -1), 70.0)
        self.assertFloatsIdentical(round_ties_to_away(2.37, -2), 0.0)
        self.assertFloatsIdentical(round_ties_to_away(2.37, -1), 0.0)
        self.assertFloatsIdentical(round_ties_to_away(-2.37, -1), -0.0)
        self.assertFloatsIdentical(round_ties_to_away(2.37, 0), 2.0)
        self.assertFloatsIdentical(round_ties_to_away(2.37, 1), 2.4)
        self.assertFloatsIdentical(round_ties_to_away(2.37, 2), 2.37)
        self.assertFloatsIdentical(round_ties_to_away(2.553, 2), 2.55)

        self.assertFloatsIdentical(round_ties_to_away(0.0, 1), 0.0)
        self.assertFloatsIdentical(round_ties_to_away(-0.0, 1), -0.0)

    def test_exact_halfway_cases(self):
        self.assertFloatsIdentical(round_ties_to_zero(2.5, 0), 2.0)
        self.assertFloatsIdentical(round_ties_to_away(2.5, 0), 3.0)
        self.assertFloatsIdentical(round_ties_to_plus(2.5, 0), 3.0)
        self.assertFloatsIdentical(round_ties_to_minus(2.5, 0), 2.0)
        self.assertFloatsIdentical(round_ties_to_even(2.5, 0), 2.0)
        self.assertFloatsIdentical(round_ties_to_odd(2.5, 0), 3.0)

        self.assertFloatsIdentical(round_ties_to_zero(3.5, 0), 3.0)
        self.assertFloatsIdentical(round_ties_to_away(3.5, 0), 4.0)
        self.assertFloatsIdentical(round_ties_to_plus(3.5, 0), 4.0)
        self.assertFloatsIdentical(round_ties_to_minus(3.5, 0), 3.0)
        self.assertFloatsIdentical(round_ties_to_even(3.5, 0), 4.0)
        self.assertFloatsIdentical(round_ties_to_odd(3.5, 0), 3.0)

        self.assertFloatsIdentical(round_ties_to_zero(-2.5, 0), -2.0)
        self.assertFloatsIdentical(round_ties_to_away(-2.5, 0), -3.0)
        self.assertFloatsIdentical(round_ties_to_plus(-2.5, 0), -2.0)
        self.assertFloatsIdentical(round_ties_to_minus(-2.5, 0), -3.0)
        self.assertFloatsIdentical(round_ties_to_even(-2.5, 0), -2.0)
        self.assertFloatsIdentical(round_ties_to_odd(-2.5, 0), -3.0)

        self.assertFloatsIdentical(round_ties_to_zero(-3.5, 0), -3.0)
        self.assertFloatsIdentical(round_ties_to_away(-3.5, 0), -4.0)
        self.assertFloatsIdentical(round_ties_to_plus(-3.5, 0), -3.0)
        self.assertFloatsIdentical(round_ties_to_minus(-3.5, 0), -4.0)
        self.assertFloatsIdentical(round_ties_to_even(-3.5, 0), -4.0)
        self.assertFloatsIdentical(round_ties_to_odd(-3.5, 0), -3.0)

    def test_special_floats(self):
        for rounding_function in ALL_ROUNDING_FUNCTIONS:
            with self.subTest(rounding_function=rounding_function):
                self.assertFloatsIdentical(rounding_function(math.nan, 0), math.nan)
                self.assertFloatsIdentical(rounding_function(math.inf, 0), math.inf)
                self.assertFloatsIdentical(rounding_function(-math.inf, 0), -math.inf)

    def test_round_finite_to_overflow(self):
        for rounding_function in MIDPOINT_ROUNDING_FUNCTIONS:
            with self.subTest(rounding_function=rounding_function):
                with self.assertRaises(OverflowError):
                    rounding_function(1.7e308, -308)
                with self.assertRaises(OverflowError):
                    rounding_function(-1.7e308, -308)

    def test_round_integers_places_none(self):
        test_values = [*range(-10, 10), *range(10 ** 100 - 10, 10 ** 100 + 10)]
        for rounding_function in MIDPOINT_ROUNDING_FUNCTIONS:
            for value in test_values:
                rounded_value = rounding_function(value)
                self.assertIntsIdentical(rounded_value, value)

    def test_round_integers_places_not_none(self):
        self.assertIntsIdentical(round_ties_to_even(123456, 1000), 123456)
        self.assertIntsIdentical(round_ties_to_even(123456, 2), 123456)
        self.assertIntsIdentical(round_ties_to_even(123456, 1), 123456)
        self.assertIntsIdentical(round_ties_to_even(123456, 0), 123456)
        self.assertIntsIdentical(round_ties_to_even(123456, -1), 123460)
        self.assertIntsIdentical(round_ties_to_even(123456, -2), 123500)
        self.assertIntsIdentical(round_ties_to_even(123456, -3), 123000)
        self.assertIntsIdentical(round_ties_to_even(123456, -5), 100000)
        self.assertIntsIdentical(round_ties_to_even(123456, -6), 0)
        self.assertIntsIdentical(round_ties_to_even(123456, -7), 0)
        self.assertIntsIdentical(round_ties_to_even(123456, -1000), 0)

    def test_round_huge_integers(self):
        # Check that we're not depending on converting integers to floats
        self.assertIntsIdentical(round_ties_to_away(2 ** 1025, 0), 2 ** 1025)
        self.assertIntsIdentical(round_to_odd(-(2 ** 1025)), -(2 ** 1025))

    def test_round_fractions_places_none(self):
        # Tests pairs for round-ties-to-even
        F = fractions.Fraction
        self.assertIntsIdentical(round_ties_to_even(F(-3, 2)), -2)
        self.assertIntsIdentical(round_ties_to_even(F(-1, 2)), 0)
        self.assertIntsIdentical(round_ties_to_even(F(1, 2)), 0)
        self.assertIntsIdentical(round_ties_to_even(F(3, 2)), 2)

        self.assertIntsIdentical(round_ties_to_away(F(1, 2)), 1)

    def test_round_fractions_places_not_none(self):
        F = fractions.Fraction
        test_value = fractions.Fraction(10000, 7)
        self.assertFractionsIdentical(round_ties_to_even(test_value, -1000), F(0))
        self.assertFractionsIdentical(round_ties_to_even(test_value, -2), F(1400))
        self.assertFractionsIdentical(round_ties_to_even(test_value, -1), F(1430))
        self.assertFractionsIdentical(round_ties_to_even(test_value, 0), F(1429))
        self.assertFractionsIdentical(round_ties_to_even(test_value, 1), F("1428.6"))
        self.assertFractionsIdentical(round_ties_to_even(test_value, 2), F("1428.57"))

        self.assertFractionsIdentical(round_ties_to_even(test_value, -1000), F(0))
        self.assertFractionsIdentical(round_to_zero(test_value, -2), F(1400))
        self.assertFractionsIdentical(round_to_zero(test_value, -1), F(1420))
        self.assertFractionsIdentical(round_to_zero(test_value, 0), F(1428))
        self.assertFractionsIdentical(round_to_zero(test_value, 1), F("1428.5"))
        self.assertFractionsIdentical(round_to_zero(test_value, 2), F("1428.57"))
        self.assertFractionsIdentical(round_to_zero(test_value, 3), F("1428.571"))

        self.assertFractionsIdentical(
            round_to_zero(test_value, 50),
            F("1428.57142857142857142857142857142857142857142857142857"),
        )

    def test_round_bool(self):
        self.assertIntsIdentical(round_ties_to_even(True), 1)
        self.assertIntsIdentical(round_ties_to_even(False), 0)

        self.assertIntsIdentical(round_ties_to_even(True, 10), 1)
        self.assertIntsIdentical(round_ties_to_even(False, -10), 0)

    def test_round_to_figures(self):
        # Rounding a nonzero number to a given number of significant figures.
        self.assertFloatsIdentical(round_to_figures(1.23456, figures=1), 1.0)
        self.assertFloatsIdentical(round_to_figures(1.23456, figures=2), 1.2)
        self.assertFloatsIdentical(round_to_figures(1.23456, figures=3), 1.23)
        self.assertFloatsIdentical(round_to_figures(1.23456, figures=4), 1.235)
        self.assertFloatsIdentical(round_to_figures(1.23456, figures=5), 1.2346)
        self.assertFloatsIdentical(round_to_figures(1.23456, figures=6), 1.23456)
        self.assertFloatsIdentical(round_to_figures(1.23456, figures=7), 1.23456)
        self.assertFloatsIdentical(round_to_figures(1.23456, figures=8), 1.23456)
        self.assertFloatsIdentical(round_to_figures(1.23456, figures=2000), 1.23456)

        self.assertFloatsIdentical(round_to_figures(-1.23456, figures=3), -1.23)
        self.assertFloatsIdentical(round_to_figures(123456.0, figures=3), 123000.0)

    def test_round_to_figures_non_positive_figures(self):
        with self.assertRaises(ValueError):
            round_to_figures(1.23456, 0)
        with self.assertRaises(ValueError):
            round_to_figures(1.23456, -1)

    def test_round_to_figures_overflow_case(self):
        with self.assertRaises(OverflowError):
            round_to_figures(1.797e308, 1)
        with self.assertRaises(OverflowError):
            round_to_figures(-1.797e308, 1)
        with self.assertRaises(OverflowError):
            round_to_figures(1.797e308, 2)
        with self.assertRaises(OverflowError):
            round_to_figures(1.797e308, 3)

    def test_round_to_figures_corner_cases(self):
        # Cases where accurate computation of ilog10(input) matters.
        # Are there actually any floating-point cases where this matters?
        # Possibly not, for rounding.

        # We're computing e = floor(log10(abs(input))). The dangers are:
        # - if "abs(input)" is just above a power of 10, e may end up one too small
        # - if "abs(input)" is just below a power of 10, e may end up one too large

        # Let's just try all the corner cases and see what happens. We'll compute
        # the smallest and the largest representable float in each decade.

        # Check extremes of each float decade.
        for e, x in DECADE_TEST_VALUES:
            # 10**e <= x < 10**(e + 1),
            # so if we want to round to 'figures' figures,
            # want to round to a multiple of 10**(e + 1 - figures)
            for figures in range(1, 20):
                with self.subTest(e=e, x=x, figures=figures):
                    try:
                        actual_result = round_to_figures(x, figures)
                    except OverflowError:
                        actual_result = math.copysign(math.inf, x)

                    try:
                        expected_result = round_ties_to_even(x, figures - e - 1)
                    except OverflowError:
                        expected_result = math.copysign(math.inf, x)

                    self.assertFloatsIdentical(actual_result, expected_result)

    # XXX Also want to cover cases where the rounding step changes the decade.

    # XXX Test other number types.

    # XXX Test infinities and nans

    # XXX Decide what to do with zeros: what's the exponent of the
    # result?

    def test_round_to_figures_ints(self):
        self.assertIntsIdentical(round_to_figures(12345, 1), 10000)
        self.assertIntsIdentical(round_to_figures(12345, 2), 12000)
        self.assertIntsIdentical(round_to_figures(12345, 3), 12300)
        self.assertIntsIdentical(round_to_figures(12345, 4), 12340)
        self.assertIntsIdentical(round_to_figures(12345, 5), 12345)
        self.assertIntsIdentical(round_to_figures(12345, 6), 12345)
        self.assertIntsIdentical(round_to_figures(12345, 7), 12345)
        self.assertIntsIdentical(round_to_figures(12345, 2000), 12345)

        self.assertIntsIdentical(round_to_figures(True, 2), 1)

    def test_round_to_figures_decimals(self):
        # Tuples (value-as-string, figures, mode, expected_result-as-string)
        test_cases = [
            ("1.25", 2, TIES_TO_EVEN, "1.2"),
            ("1.25", 3, TIES_TO_EVEN, "1.25"),
            ("1.25", 4, TIES_TO_EVEN, "1.250"),
            ("9.9999", 4, TIES_TO_EVEN, "10.00"),
            # Should be able to handle huge decimal instances without problems.
            # This double checks that we're not using to-fraction fallbacks.
            ("1e9999999999", 4, TIES_TO_EVEN, "1.000e9999999999"),
            # Also check values with more digits than the context precision,
            # to double check that we're not losing digits (e.g., by doing abs).
            # We shouldn't be making any use of the local context.
            # Might also want to add some tests with the context deliberately
            # set to something odd (rounding mode, precision, emin, emax) to
            # make sure that the context isn't being used.
            ("1" * 100, 100, TIES_TO_EVEN, "1" * 100),
        ]

        for case in test_cases:
            with self.subTest(case=case):
                value, figures, mode, expected_result = case
                value = decimal.Decimal(value)
                expected_result = decimal.Decimal(expected_result)
                self.assertDecimalsIdentical(
                    round_to_figures(value, figures, mode=mode),
                    expected_result,
                )

    def test_round_to_figures_other_rounding_modes(self):
        # Tuples (value, figures, mode, expected_result)
        test_cases = [
            (1.25, 2, TIES_TO_EVEN, 1.2),
            (1.75, 2, TIES_TO_EVEN, 1.8),
            (-1.25, 2, TIES_TO_EVEN, -1.2),
            (-1.75, 2, TIES_TO_EVEN, -1.8),
            (1.25, 2, TIES_TO_ODD, 1.3),
            (1.75, 2, TIES_TO_ODD, 1.7),
            (-1.25, 2, TIES_TO_ODD, -1.3),
            (-1.75, 2, TIES_TO_ODD, -1.7),
            (1.25, 2, TIES_TO_AWAY, 1.3),
            (1.75, 2, TIES_TO_AWAY, 1.8),
            (-1.25, 2, TIES_TO_AWAY, -1.3),
            (-1.75, 2, TIES_TO_AWAY, -1.8),
            (1.25, 2, TIES_TO_ZERO, 1.2),
            (1.75, 2, TIES_TO_ZERO, 1.7),
            (-1.25, 2, TIES_TO_ZERO, -1.2),
            (-1.75, 2, TIES_TO_ZERO, -1.7),
            (1.25, 2, TIES_TO_PLUS, 1.3),
            (1.75, 2, TIES_TO_PLUS, 1.8),
            (-1.25, 2, TIES_TO_PLUS, -1.2),
            (-1.75, 2, TIES_TO_PLUS, -1.7),
            (1.25, 2, TIES_TO_MINUS, 1.2),
            (1.75, 2, TIES_TO_MINUS, 1.7),
            (-1.25, 2, TIES_TO_MINUS, -1.3),
            (-1.75, 2, TIES_TO_MINUS, -1.8),
        ]

        for case in test_cases:
            with self.subTest(case=case):
                value, figures, mode, expected_result = case
                self.assertEqual(
                    round_to_figures(value, figures, mode=mode),
                    expected_result,
                )

    def assertIntsIdentical(self, first, second):
        self.assertEqual(type(first), int)
        self.assertEqual(type(second), int)
        self.assertEqual(first, second)

    def assertFractionsIdentical(self, first, second):
        self.assertEqual(type(first), fractions.Fraction)
        self.assertEqual(type(second), fractions.Fraction)
        self.assertEqual(first, second)

    def assertFloatsIdentical(self, first, second):
        self.assertEqual(type(first), float)
        self.assertEqual(type(second), float)

        if math.isnan(first) and math.isnan(second):
            return

        self.assertEqual(first, second)
        if first == 0.0:
            self.assertEqual(sign_bit(first), sign_bit(second))

    def assertDecimalsIdentical(self, first, second):
        self.assertEqual(type(first), decimal.Decimal)
        self.assertEqual(type(second), decimal.Decimal)

        self.assertEqual(str(first), str(second))
