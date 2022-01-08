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
from ...solfege import DODIRERI_IT

_OUTBOUND = tuple(
    r'do di re ri mi fa fi so si la li ti '\
    r'do ti te la le so se fa mi me re ra'.split()
)

_INBOUND = (
    (0, 0), (0, +1), (1, 0), (1, +1), (2, 0), (3, 0), (3, +1), (4, 0),
    (4, +1), (5, 0), (5, +1), (6, 0),
    (0, 0), (6, 0), (6, -1), (5, 0), (5, -1), (4, 0), (4, -1), (3, 0),
    (2, 0), (2, -1), (1, 0), (1, -1), 
)


class T(TestCase):
    def _test(self, feed, expected):
        actual = tuple(DODIRERI_IT[y] for y in feed)
        self.assertEqual(expected, actual)

    def test0(self):
        self._test(_OUTBOUND, _INBOUND)

    def test1(self):
        self._test(_INBOUND, _OUTBOUND)
