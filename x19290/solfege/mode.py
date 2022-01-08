# Copyright (C) 2021 Hiroki Horiuchi <x19290@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# TODO: many for "modes"

from . import OCT_7 as _N_MODES
from ..lib.protecteddict import ProtectedDict


class ModesNs(ProtectedDict):
    setup_globals = modes = None

    def __init__(self, mode):
        from .pitch import KEY_NAMES, SEMITONE

        def define_class(keyname):
            from .pitch import Pitch, KEY_SIGNATURES
            from . import CDEFGAB
            from ..lib.charseq import ROMAN_ONE2TEN

            keyname, semitone = keyname.title(), SEMITONE[keyname[1:]]
            signature, number, textart = KEY_SIGNATURES[keyname]
            do = CDEFGAB[keyname[:1]]
            attributes = dict(
                do=do, semitone=semitone, mode=mode,
                modesep=keyname.__len__(), signature=signature, number=number,
                textart=textart,
            )
            modestr = ROMAN_ONE2TEN[mode] if mode else r''
            classname = keyname + modestr
            clazz = type(classname, (Pitch,), attributes)
            return clazz

        super(ModesNs, self).__init__()
        mutable = self.mutable
        for keyname in KEY_NAMES:
            clazz = define_class(keyname)
            mutable[clazz.__name__] = define_class(keyname)


def _setup_globals(global_ns):
    from .pitch import ACCIDENTAL2SAFECHAR, MODESTRS

    def make_modealias(modenum: int, modestr=None):
        if modestr is None:
            modestr = MODESTRS[modenum]
        to_safe = ACCIDENTAL2SAFECHAR.mutable
        for realname, clazz in _MODES[modenum].mutable.items():
            realshift = realname[1:clazz.modesep]
            safeshift = to_safe[realshift]
            assert safeshift != realshift
            safename = realname[:1] + safeshift + modestr
            assert safename != realname
            global_ns[safename] = global_ns[realname] = clazz

    for mode in range(_MODES.__len__()):
        make_modealias(mode)
    make_modealias(0, r'')

_MODES = tuple(map(ModesNs, range(_N_MODES)))

ModesNs.setup_globals = _setup_globals
ModesNs.modes = _MODES
