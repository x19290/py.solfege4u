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
from ...lib.centered import CenteredStr
from ...lib.resolver import CenteredStrResolver

_FEED0 = CenteredStr(r'abc')
_FEED1 = CenteredStrResolver(r'abc')


class T(TestCase):
    def _test(self, centered):
        expected = r'a b c'
        actual = r' '.join(centered[y] for y in range(-1, 2))
        self.assertEqual(expected, actual)

    def test0(self):
        self._test(_FEED0)

    def test1(self):
        self._test(_FEED1)

    def test2(self):
        expected = -1, 0, +1
        actual = tuple(_FEED1[y] for y in r'abc')
        self.assertEqual(expected, actual)