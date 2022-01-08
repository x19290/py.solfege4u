# Copyright (C) 2021 Hiroki Horiuchi <x19290@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from .mode import ModesNs
from .pitch import Pitch
from ..lib.ranged import Ranged

r'''
♭: f (flat)
♮: n (natural)
♯: s (sharp)

Ⅰ: _1
Ⅱ: _2
Ⅲ: _3
Ⅳ: _4
Ⅴ: _5
Ⅵ: _6
Ⅶ: _7
'''

A = B = C = D = E = F = G =\
    An = Bn = Cn = Dn = En = Fn = Gn =\
\
    A_1 = B_1 = C_1 = D_1 = E_1 = F_1 = G_1 =\
    An_1 = Bn_1 = Cn_1 = Dn_1 = En_1 = Fn_1 = Gn_1 =\
\
    A_2 = B_2 = C_2 = D_2 = E_2 = F_2 = G_2 =\
    An_2 = Bn_2 = Cn_2 = Dn_2 = En_2 = Fn_2 = Gn_2 =\
\
    A_3 = B_3 = C_3 = D_3 = E_3 = F_3 = G_3 =\
    An_3 = Bn_3 = Cn_3 = Dn_3 = En_3 = Fn_3 = Gn_3 =\
\
    A_4 = B_4 = C_4 = D_4 = E_4 = F_4 = G_4 =\
    An_4 = Bn_4 = Cn_4 = Dn_4 = En_4 = Fn_4 = Gn_4 =\
\
    A_5 = B_5 = C_5 = D_5 = E_5 = F_5 = G_5 =\
    An_5 = Bn_5 = Cn_5 = Dn_5 = En_5 = Fn_5 = Gn_5 =\
\
    A_6 = B_6 = C_6 = D_6 = E_6 = F_6 = G_6 =\
    An_6 = Bn_6 = Cn_6 = Dn_6 = En_6 = Fn_6 = Gn_6 =\
\
    A_7 = B_7 = C_7 = D_7 = E_7 = F_7 = G_7 =\
    An_7 = Bn_7 = Cn_7 = Dn_7 = En_7 = Fn_7 = Gn_7 =\
\
    Df = Cs = Ef = Gf = Fs = Af = Bf = Cf =\
\
    Df_1 = Cs_1 = Ef_1 = Gf_1 = Fs_1 = Af_1 = Bf_1 = Cf_1 =\
    Df_2 = Cs_2 = Ef_2 = Gf_2 = Fs_2 = Af_2 = Bf_2 = Cf_2 =\
    Df_3 = Cs_3 = Ef_3 = Gf_3 = Fs_3 = Af_3 = Bf_3 = Cf_3 =\
    Df_4 = Cs_4 = Ef_4 = Gf_4 = Fs_4 = Af_4 = Bf_4 = Cf_4 =\
    Df_5 = Cs_5 = Ef_5 = Gf_5 = Fs_5 = Af_5 = Bf_5 = Cf_5 =\
    Df_6 = Cs_6 = Ef_6 = Gf_6 = Fs_6 = Af_6 = Bf_6 = Cf_6 =\
    Df_7 = Cs_7 = Ef_7 = Gf_7 = Fs_7 = Af_7 = Bf_7 = Cf_7 =\
\
    Pitch


ModesNs.setup_globals(globals())

_KEY_CLOCKS_SRC = r'''
C♮   G♮ D♮ A♮ E♮ B♮ F♯ C♯   A♭ E♭ B♭ F♮
C♮   G♮ D♮ A♮ E♮ B♮ F♯   D♭ A♭ E♭ B♭ F♮
C♮   G♮ D♮ A♮ E♮ B♮   G♭ D♭ A♭ E♭ B♭ F♮
C♮   G♮ D♮ A♮ E♮   C♭ G♭ D♭ A♭ E♭ B♭ F♮
'''[1:]

def __key_clocks_txt():
    def key(y):
        if y == r'C♭':
            rv = 7, None  # large enough
        else:
            from .pitch import ACCIDENTAL
            from . import CDEFGAB
            rv = CDEFGAB[y[0]], ACCIDENTAL[y[1:]]
        return rv

    for y in _KEY_CLOCKS_SRC.splitlines(keepends=False):
        y = y.split()
        y.sort(key=key)
        y = r' '.join(y)
        # the following is currently required. this must be a bug
        y = y.replace(r'♭', r'f').replace(r'♮', r'n').replace(R'♯', r's')
        yield y


# _KEY_CLOCKS_TXT = r'''
# C♮ C♯ D♮ E♭ E♮ F♮ F♯ G♮ A♭ A♮ B♭ B♮
# C♮ D♭ D♮ E♭ E♮ F♮ F♯ G♮ A♭ A♮ B♭ B♮
# C♮ D♭ D♮ E♭ E♮ F♮ G♭ G♮ A♭ A♮ B♭ B♮
# C♮ D♭ D♮ E♭ E♮ F♮ G♭ G♮ A♭ A♮ B♭ C♭
# '''[1:]
_KEY_CLOCKS_TXT = '\n'.join(__key_clocks_txt())


def __key_clocks():
    ns = globals()
    for clock in _KEY_CLOCKS_TXT.splitlines(keepends=False):
        yield tuple(ns[y] for y in clock.split())

r'''
key clock and `_KEY_CLOCKS` are currently internal ideas.
no plan to export them

_KEY_CLOCKS[P.maxflats == 4] == clock for P
_KEY_CLOCKS[Q.maxflats == 5] == clock for Q
_KEY_CLOCKS[R.maxflats == 6] == clock for R
_KEY_CLOCKS[S.maxflats == 7] == clock for S
'''


class _KeyClocks(Ranged):
    start, stop = 4, 8


_KEY_CLOCKS = _KeyClocks(__key_clocks())


class Hour(int):
    r'''
    makes it possible to transpose somethings by semitones.
    7 hours == perfect 5th.
    there are four subclasses `P`, `Q`, `R`, `S` of `Hour.`
    '''
    def __add__(self, another):
        from .pitch import Pitch
        from . import PERFECT5TH_SEMITONES

        if isinstance(another, Pitch):
            # c4, g4 = C(4, r'do'), G(4, r'do')
            # P(7) + c4 == g4
            clazz = another.__class__
            i = (clazz.number * PERFECT5TH_SEMITONES + self) % 12
            rv = _KEY_CLOCKS[self.maxflats][i](*another)
        elif isinstance(another, type) and issubclass(another, Pitch):
            # P(7) + C == G
            i = (another.number * PERFECT5TH_SEMITONES + self) % 12
            rv = _KEY_CLOCKS[self.maxflats][i]
        else:
            # P(0) + 7 == P(7)
            rv = self.__class__(super(Hour, self).__add__(another))
        return rv

    def __eq__(self, another):
        # TODO: test
        return self.__class__ is another.__class__ and\
            super(Hour, self).__eq__(another)

    def __ne__(self, another):
        return not self.__eq_(another)

    def __hash__(self):
        return super(Hour, self).__hash__()


class P(Hour):
    r'''
    Gn Dn An En Bn Fs Cs   Af Ef Bf Fn
    '''
    maxsharps, maxflats = 7, 4


class Q(Hour):
    r'''
    Gn Dn An En Bn Fs   Df Af Ef Bf Fn
    '''
    maxsharps, maxflats = 6, 5


class R(Hour):
    r'''
    Gn Dn An En Bn   Gf Df Af Ef Bf Fn
    '''
    maxsharps, maxflats = 5, 6


class S(Hour):
    r'''
    Gn Dn An En   Cf Gf Df Af Ef Bf Fn
    '''
    maxsharps, maxflats = 4, 7


NS = globals()
