# Copyright (C) 2021 Hiroki Horiuchi <x19290@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from ...solfege.ns import C, Cn, Cf, Cs_2, B, Bn, Bf, Bf_7, C_1, D, Cf
from .. import TestBase


class T0class(TestBase):
    feed = C, Cn, Cf, Cs_2, B, Bn, Bf, Bf_7

    def test0name(self):
        expected = r'C C C♭ C♯Ⅱ B B B♭ B♭Ⅶ'
        actual = r' '.join(y.__name__ for y in self.feed)
        self.assertEqual(expected, actual)

    def test1butmode(self):
        expected = r'C C C♭ C♯ B B B♭ B♭'
        actual = r' '.join(y.__name__[:y.modesep] for y in self.feed)
        self.assertEqual(expected, actual)

    def test2mode(self):
        expected = r',,,Ⅱ,,,,Ⅶ'
        actual = r','.join(y.__name__[y.modesep:] for y in self.feed)
        self.assertEqual(expected, actual)


class T1instance(TestBase):
    def test0(self):
        c0, c1 = C(4, 0), C(4, 0)
        self.assertEqual(c0, c1)

    def test1(self):
        c, d = (C(4, y) for y in range(2))
        self.assertNotEqual(c, d)

    def test2(self):
        x, y, z = C_1(4, 0), D(4, 0), C_1(4, 1)
        expected = True, False, False
        actual = tuple(x) == tuple(y), x == y, y == z
        self.assertEqual(expected, actual)


class T2render(TestBase):
    def _test(self, feed, expected):
        actual = r' '.join(y.__str__() for y in feed)
        self.assertEqual(expected, actual)

    def test0(self):
        _ = D(4, 1, 0)
        _ = _.__str__()
        feed = (D(4, y, 0) for y in range(3))
        self._test(feed, r'D4 E4 F4')

    def test1(self):
        feed = (Cf(4, 0, y).__str__() for y in range(-1, 2))
        self._test(feed, r'C𝄫4 C4 C♮4')

    def test3(self):
        feed = expected = r'C♯4'
        actual = C.parse(feed).__str__()
        self.assertEqual(expected, actual)