# Copyright (C) 2021 Hiroki Horiuchi <x19290@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

r'''
test if keyaliases: *str in `NS` are right
'''

from ...solfege.pitch import Pitch, _KEY_SIGNATURES
from ...solfege.ns import NS
from ...solfege import OCT_7
from ...lib.strictset import StrictSet
from .. import TestBase
from itertools import product


def __keyname_pats():
    from re import compile

    official = r'[A-G][♭♯]?(?:[ⅡⅢⅣⅤⅥⅦ]|)'
    safe = r'[A-G][fns]?(?:_[1-7]|)'
    yield from (compile(r'^%s$' % y) for y in (official, safe))


def __actual():
    official, safe = StrictSet(), StrictSet()
    for k, v in NS.items():
        if isinstance(v, type) and k != r'Pitch' and issubclass(v, Pitch):
            if _PAT_OFFICIAL.match(k):
                official.add(k)
            elif _PAT_SAFE.match(k):
                safe.add(k)
            else:
                raise AssertionError
    yield from (tuple(sorted(y)) for y in (official, safe))


def __expected():
    r'''
    ALIAS: NAME + MODE
    ALIASES: NAMES * MODES

    NS[ALIAS] == C,... B♭Ⅶ, BⅦ

    C is NS['C']
    Bf_7 is NS['B♭Ⅶ']

    C.__name__ == 'C'
    Bf_7.__name__ == 'B♭Ⅶ'

    officialnames: 'C',... 'B♭', 'B'
    safenames: ('Cf', 'C', 'Cs',... 'Bf', 'B') + ('Cn',... 'Bn')
    officialmodes: '', + 'Ⅱ',... 'Ⅶ'
    safemodes: '', '_1',... '_7'
    commonaliases: 'C',... 'B'
    safealiases = safenames * safemodes - commonaliases
    '''

    #{ _xlen: expected length
    officialnames_xlen = 15
    safenames_xlen = officialnames_xlen + OCT_7
    officialmodes_xlen = OCT_7
    safemodes_xlen = 1 + OCT_7
    commonaliases_xlen = 1 * min(officialmodes_xlen, safemodes_xlen)
    officialaliases_xlen = officialnames_xlen * officialmodes_xlen
    safealiases_w_extra_xlen = safenames_xlen * safemodes_xlen
    safealiases_xlen = safealiases_w_extra_xlen - commonaliases_xlen
    #}

    g = _KEY_SIGNATURES.splitlines(keepends=False)
    officialnames = tuple(y.split()[0] for y in g)
    assert officialnames.__len__() == officialnames_xlen

    def safenames():
        for y in officialnames:
            y = y.replace(r'♭', r'f').replace(r'♯', r's')
            yield y  # names_xlen times
            if y.__len__() == 1:
                yield y + r'n'  # OCT_7 times

    safenames = tuple(safenames())
    assert safenames.__len__() == safenames_xlen

    officialmodes = (r'',) + tuple(r'ⅡⅢⅣⅤⅥⅦ')
    assert officialmodes.__len__() == officialmodes_xlen

    safemodes = (r'',) + tuple(r'_%d' % y for y in range(1, 8))
    assert safemodes.__len__() == safemodes_xlen

    officialaliases = (y[0] + y[1] for y
        in product(officialnames, officialmodes)
    )
    officialaliases = tuple(sorted(officialaliases))
    assert officialaliases.__len__() == set(officialaliases).__len__() ==\
        officialaliases_xlen

    safealiases_w_extra = tuple(
        y[0] + y[1] for y in product(safenames, safemodes)
    )

    commonaliases = (y for y in safealiases_w_extra if _PAT_OFFICIAL.match(y))
    commonaliases = tuple(sorted(commonaliases))
    assert commonaliases.__len__() == commonaliases_xlen

    safealiases = (
        y for y in safealiases_w_extra if not _PAT_OFFICIAL.match(y)
    )
    safealiases = tuple(sorted(safealiases))
    assert safealiases.__len__() == set(safealiases).__len__() ==\
        safealiases_xlen

    yield from (officialaliases, safealiases)


_PAT_OFFICIAL, _PAT_SAFE = __keyname_pats()
_EXPECTED_OFFICIAL, _EXPECTED_SAFE = (tuple(sorted(y)) for y in __expected())
_ACTUAL_OFFICIAL, _ACTUAL_SAFE = __actual()


class T(TestBase):
    def test0(self):
        self.assertEqual(_EXPECTED_OFFICIAL, _ACTUAL_OFFICIAL)

    def test1(self):
        self.assertEqual(_EXPECTED_SAFE, _ACTUAL_SAFE)
