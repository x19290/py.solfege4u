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
from ...solfege.semitone import basic_semitones
from ...solfege import OCT_7
from .. import TestBase


class T0(TestBase):
    def test0(self):
        feed = r'do di re ri mi fa fi so si la li ti'
        feed = (Cn(4, y)[1:] for y in feed.split())
        actual = tuple(basic_semitones(*y) for y in feed)
        expected = tuple(range(12))
        self.assertEqual(expected, actual)

    def test1(self):
        feed = (0, 0), (0, 1), (1, 0), (1, 1), (2, 0),\
            (3, 0), (3, 1), (4, 0), (4, 1), (5, 0), (5, 1), (6, 0)
        actual = tuple(basic_semitones(*y) for y in feed)
        expected = tuple(range(12))
        self.assertEqual(expected, actual)

    def test2(self):
        feed = r'do+1 ti te la le so se fa mi me re ra'
        feed = (Cn(4, y)[1:] for y in feed.split())
        actual = tuple(basic_semitones(*y) for y in feed)
        expected = (0,) + tuple(range(11, 0, -1))
        self.assertEqual(expected, actual)

    def test3(self):
        feed = (7, 0),\
            (6, 0), (6, -1), (5, 0), (5, -1), (4, 0), (4, -1), (3, 0),\
            (2, 0), (2, -1), (1, 0), (1, -1)
        actual = tuple(basic_semitones(*y) for y in feed)
        expected = (0,) + tuple(range(11, 0, -1))
        self.assertEqual(expected, actual)

class T1(TestBase):
    def test0(self):
        expected = 48, 60
        actual = tuple(Cn.parse(y).homogenize() for y in r'C4 C5'.split())
        self.assertEqual(expected, actual)

    def test1(self):
        expected = 50, 62
        actual = tuple(Dn.parse(y).homogenize() for y in r'D4 D5'.split())
        self.assertEqual(expected, actual)

    def test2(self):
        expected = 61, 73
        actual = tuple(Dn.parse(y).homogenize() for y in r'C4 C5'.split())
        self.assertEqual(expected, actual)

    def test3(self):
        expected = 47, 59
        actual = tuple(Cf.parse(y).homogenize() for y in r'C4 C5'.split())
        self.assertEqual(expected, actual)


class T2(TestBase):
    def _test(self, key, feed, start, stop):
        actual = tuple(key.parse(y).homogenize() for y in feed.split())
        step = -1 if stop < start else 1
        expected = tuple(range(start, stop, step))
        self.assertEqual(expected, actual)

    def test0cn0asc(self):
        self._test(Cn, r'C4 C♯4 D4 D♯4 E4 F4 F♯4 G4 G♯4 A4 A♯4 B4', 48, 60)

    def test0cn1dsc(self):
        self._test(Cn, r'C5 B4 B♭4 A4 A♭4 G4 G♭4 F4 E4 E♭4 D4 D♭4', 60, 48)

    def test1dn0asc(self):
        self._test(Dn, r'D4 D♯4 E4 E♯4 F4 G4 G♯4 A4 A♯4 B4 B♯4 C4', 50, 62)

    def test1dn1dsc(self):
        self._test(Dn, r'D5 C4 C♮4 B4 B♭4 A4 A♭4 G4 F4 F♮4 E4 E♭4', 62, 50)

    def test2cs0asc(self):
        self._test(Cs, r'C4 C𝄪4 D4 D𝄪4 E4 F4 F𝄪4 G4 G𝄪4 A4 A𝄪4 B4', 49, 61)

    def test2cs1dsc(self):
        self._test(Cs, r'C5 B4 B♮4 A4 A♮4 G4 G♮4 F4 E4 E♮4 D4 D♮4', 61, 49)

    def test3fs0asc(self):
        self._test(Fs, r'F4 F𝄪4 G4 G𝄪4 A4 B4 B♯4 C4 C𝄪4 D4 D𝄪4 E4', 54, 66)

    def test3fs1dsc(self):
        self._test(Fs, r'F5 E4 E♮4 D4 D♮4 C4 C♮4 B4 A4 A♮4 G4 G♮4', 66, 54)

    def test4cf0asc(self):
        self._test(Cf, r'C4 C♮4 D4 D♮4 E4 F4 F♮4 G4 G♮4 A4 A♮4 B4', 47, 59)

    def test4cf1dsc(self):
        self._test(Cf, r'C5 B4 B𝄫4 A4 A𝄫4 G4 G𝄫4 F4 E4 E𝄫4 D4 D𝄫4', 59, 47)