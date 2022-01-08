# Copyright (C) 2021 Hiroki Horiuchi <x19290@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from ..lib.ring import RingMixin
from ..lib.resolver import StrResolver
from ..lib.roundtripdict import RoundtripDict


class _Ring(RingMixin, StrResolver):
    def __new__(cls):
        return super(_Ring, cls).__new__(cls, r'CDEFGAB')

    def _resolve(self, c):
        return ord(c) - ORD_C


ORD_C = ord(r'C')
CDEFGAB = _Ring()
OCT_7 = CDEFGAB.__len__()
PERFECT5TH_SEMITONES = 7

r'''
dodireri: movable do
solfege: the fixed do system of Shearer

english pronunciations are taken
    partially from https://www.aaronshearerfoundation.org/site/solfege/ and
    partially from https://en.wikipedia.org/wiki/Solf%C3%A8ge
'''

DODIRERI_IT = RoundtripDict(
    do=(0, 0), re=(1, 0), mi=(2, 0),
    fa=(3, 0), so=(4, 0), la=(5, 0), ti=(6, 0),

    di=(0, +1), ri=(1, +1), fi=(3, +1), si=(4, +1), li=(5, +1),
    ra=(1, -1), me=(2, -1), se=(4, -1), le=(5, -1), te=(6, -1), 
)
DODIRERI_EN = RoundtripDict(
    doh=(0, 0), ray=(1, 0), mee=(2, 0),
    fah=(3, 0), soh=(4, 0), lah=(5, 0), tee=(6, 0),

    dee=(0, +1), ree=(1, +1), fee=(3, +1), see=(4, +1), lee=(5, +1),
    rah=(1, -1), may=(2, -1), say=(4, -1), lay=(5, -1), tay=(6, -1), 
)

_SOLFEGE_IT = r'''
Dau De Do  Di Dai
Rau Ra Re  Ri Rai
Mau Me Mi  Ma Mai
Fau Fe Fa  Fi Fai
Sau Se Sol Si Sai
Lau Le La  Li Lai
Tau Te Ti  Ta Tai
'''[1:]
_SOLFEGE_EN = r'''
Daw Day Doh Dee Dai
Raw Rah Ray Ree Rai
Maw May Mee Mah Mai
Faw Fay Fah Fee Fai
Saw Say Soh See Sai
Law Lay Lah Lee Lai
Taw Tay Tee Tah Tai
'''[1:]


def _solfege_rows(text):
    from ..lib.centered import Centered
    for row in text.splitlines(keepends=False):
        yield Centered(row.split())


SOLFEGE_EN, SOLFEGE_IT = (
    tuple(_solfege_rows(y)) for y in (_SOLFEGE_EN, _SOLFEGE_IT)
)
