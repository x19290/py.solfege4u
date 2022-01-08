# Copyright (C) 2021 Hiroki Horiuchi <x19290@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from unittest import TestCase
from ...solfege.ns import C, Cs, Df, P, S


class T(TestCase):
    def test0(self):
        expected = Cs, Df
        actual = P(1) + C, S(1) + C
        self.assertEqual(expected, actual)

    def test1(self):
        c4, cs4 = C(4, 0), Cs(4, 0)
        feed, expected = c4, cs4
        actual = P(1) + feed
        self.assertEqual(actual, expected)