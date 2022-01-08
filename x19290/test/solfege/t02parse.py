# Copyright (C) 2021 Hiroki Horiuchi <x19290@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from ...solfege.ns import Cn, Dn, Cs, Fs, Cf
from .. import TestBase


class T0(TestBase):
    def test0(self):
        expected = (4, 0, 0), (5, 0, 0)
        actual = tuple(tuple(Cn.parse(y)) for y in r'C4 C5'.split())
        self.assertEqual(expected, actual)


class T1roundtrip(TestBase):
    def _test(self, key, expected):
        r'''
        assert key.parse(s).__str__() == s
        '''
        feed = expected.split()
        expected = feed
        actual = [key.parse(y).__str__() for y in feed]
        self.assertEqual(expected, actual)

    def test0(self):
        self._test(
            Cn,
            r'C4 C♯4 D4 D♯4 E4 F4 F♯4 G4 G♯4 A4 A♯4 B4 '
            r'C4 B4 B♭4 A4 A♭4 G4 G♭4 F4 E4 E♭4 D4 D♭4'
        )

    def test1(self):
        self._test(
            Dn,
            r'D4 D♯4 E4 E♯4 F4 G4 G♯4 A4 A♯4 B4 B♯4 C4 '
            r'D4 C4 C♮4 B4 B♭4 A4 A♭4 G4 F4 F♮4 E4 E♭4'
        )

    def test2(self):
        self._test(
            Cs,
            r'C4 C𝄪4 D4 D𝄪4 E4 F4 F𝄪4 G4 G𝄪4 A4 A𝄪4 B4 '
            r'C4 B4 B♮4 A4 A♮4 G4 G♮4 F4 E4 E♮4 D4 D♮4'
        )

    def test1(self):
        self._test(
            Fs,
            r'F4 F𝄪4 G4 G𝄪4 A4 B4 B♯4 C4 C𝄪4 D4 D𝄪4 E4 '
            r'F4 E4 E♮4 D4 D♮4 C4 C♮4 B4 A4 A♮4 G4 G♮4'
        )

    def test1(self):
        self._test(
            Cf,
            r'C4 C♮4 D4 D♮4 E4 F4 F♮4 G4 G♮4 A4 A♮4 B4 '
            r'C5 B4 B𝄫4 A4 A𝄫4 G4 G𝄫4 F4 E4 E𝄫4 D4 D𝄫4'
        )