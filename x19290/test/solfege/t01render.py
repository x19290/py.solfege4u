# Copyright (C) 2021 Hiroki Horiuchi <x19290@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from ...solfege.ns import (
    Cn, Dn, En, Fn, Gn, An, Bn,
    Cs, Fs,
    Df, Ef, Gf, Af, Bf, Cf,
)
from .. import TestBase

r'''
C  ♮♮♮♮♮♮♮
D♭ ♭♭♮♭♭♭♮
C♯ ♯♯♯♯♯♯♯
D  ♮♮♯♮♮♮♯
E♭ ♭♮♮♭♭♮♮
E  ♮♯♯♮♮♯♯
F  ♮♮♮♭♮♮♮
G♭ ♭♭♭♭♭♭♮
F♯ ♯♯♯♮♯♯♯
G  ♮♮♮♮♮♮♯
A♭ ♭♭♮♭♭♮♮
A  ♮♮♯♮♮♯♯
B♭ ♭♮♮♭♮♮♮
C♭ ♭♭♭♭♭♭♭
B  ♮♯♯♮♯♯♯
'''[1:]


def __feed():
    asc = r'C C♯ D D♯ E F F♯ G G♯ A A♯ B'
    dsc = r'C B B♭ A A♭ G G♭ F E E♭ D D♭'

    def parse(s):
        from ...solfege.pitch import SEMITONE
        from ...solfege import CDEFGAB
        stem, accidental = s[:1], s[1:]
        pitch = CDEFGAB[stem]
        accidental = SEMITONE[accidental]
        return 4, pitch, accidental

    return map(parse, (asc + r' ' + dsc).split())


_FEED = tuple(__feed())


class T(TestBase):
    def _test(self, key, expected):
        actual = r' '.join(y.__str__() for y in (key(*y) for y in _FEED))
        self.assertEqual(expected, actual)

    def test00cn(self):
        self._test(
            Cn,
            r'C4 C♯4 D4 D♯4 E4 F4 F♯4 G4 G♯4 A4 A♯4 B4 '
            r'C4 B4 B♭4 A4 A♭4 G4 G♭4 F4 E4 E♭4 D4 D♭4',
        )

    def test01Dn(self):
        self._test(  # D E F# G A B C# D
            Dn,
            r'D4 D♯4 E4 E♯4 F4 G4 G♯4 A4 A♯4 B4 B♯4 C4 '
            r'D4 C4 C♮4 B4 B♭4 A4 A♭4 G4 F4 F♮4 E4 E♭4',
        )

    def test02En(self):
        self._test(  # E F# G# A B C# D#
            En,
            r'E4 E♯4 F4 F𝄪4 G4 A4 A♯4 B4 B♯4 C4 C𝄪4 D4 '
            r'E4 D4 D♮4 C4 C♮4 B4 B♭4 A4 G4 G♮4 F4 F♮4',
        )

    def test03Fn(self):
        self._test(  # E F# G# A B C# D#
            Fn,
            r'F4 F♯4 G4 G♯4 A4 B4 B♮4 C4 C♯4 D4 D♯4 E4 '
            r'F4 E4 E♭4 D4 D♭4 C4 C♭4 B4 A4 A♭4 G4 G♭4'
        )

    def test04Gn(self):
        self._test(  # E F# G# A B C# D#
            Gn,
            r'G4 G♯4 A4 A♯4 B4 C4 C♯4 D4 D♯4 E4 E♯4 F4 '
            r'G4 F4 F♮4 E4 E♭4 D4 D♭4 C4 B4 B♭4 A4 A♭4'
        )

    def test05An(self):
        self._test(  # E F# G# A B C# D#
            An,
            r'A4 A♯4 B4 B♯4 C4 D4 D♯4 E4 E♯4 F4 F𝄪4 G4 '
            r'A4 G4 G♮4 F4 F♮4 E4 E♭4 D4 C4 C♮4 B4 B♭4'
        )

    def test06Bn(self):
        self._test(  # E F# G# A B C# D#
            Bn,
            r'B4 B♯4 C4 C𝄪4 D4 E4 E♯4 F4 F𝄪4 G4 G𝄪4 A4 '
            r'B4 A4 A♮4 G4 G♮4 F4 F♮4 E4 D4 D♮4 C4 C♮4'
        )

    def test10cs(self):
        self._test(
            Cs,
            r'C4 C𝄪4 D4 D𝄪4 E4 F4 F𝄪4 G4 G𝄪4 A4 A𝄪4 B4 '
            r'C4 B4 B♮4 A4 A♮4 G4 G♮4 F4 E4 E♮4 D4 D♮4',
        )

    def test11fs(self):
        self._test(
            Fs,
            r'F4 F𝄪4 G4 G𝄪4 A4 B4 B♯4 C4 C𝄪4 D4 D𝄪4 E4 '
            r'F4 E4 E♮4 D4 D♮4 C4 C♮4 B4 A4 A♮4 G4 G♮4',
        )

    def test20cf(self):
        self._test(
            Cf,
            r'C4 C♮4 D4 D♮4 E4 F4 F♮4 G4 G♮4 A4 A♮4 B4 '
            r'C4 B4 B𝄫4 A4 A𝄫4 G4 G𝄫4 F4 E4 E𝄫4 D4 D𝄫4',
        )

    def test21df(self):
        self._test(
            Df,
            r'D4 D♮4 E4 E♮4 F4 G4 G♮4 A4 A♮4 B4 B♮4 C4 '
            r'D4 C4 C♭4 B4 B𝄫4 A4 A𝄫4 G4 F4 F♭4 E4 E𝄫4',
        )

    def test22ef(self):
        self._test(
            Ef,
            r'E4 E♮4 F4 F♯4 G4 A4 A♮4 B4 B♮4 C4 C♯4 D4 '
            r'E4 D4 D♭4 C4 C♭4 B4 B𝄫4 A4 G4 G♭4 F4 F♭4',
        )

    def test23gf(self):
        self._test(
            Gf,
            r'G4 G♮4 A4 A♮4 B4 C4 C♮4 D4 D♮4 E4 E♮4 F4 '
            r'G4 F4 F♭4 E4 E𝄫4 D4 D𝄫4 C4 B4 B𝄫4 A4 A𝄫4',
        )

    def test24af(self):
        self._test(
            Af,
            r'A4 A♮4 B4 B♮4 C4 D4 D♮4 E4 E♮4 F4 F♯4 G4 '
            r'A4 G4 G♭4 F4 F♭4 E4 E𝄫4 D4 C4 C♭4 B4 B𝄫4',
        )

    def test25bf(self):
        self._test(
            Bf,
            r'B4 B♮4 C4 C♯4 D4 E4 E♮4 F4 F♯4 G4 G♯4 A4 '
            r'B4 A4 A♭4 G4 G♭4 F4 F♭4 E4 D4 D♭4 C4 C♭4',
        )