# Copyright (C) 2021 Hiroki Horiuchi <x19290@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.


def textartdemo_main():
    from . import shared_opts
    from argparse import ArgumentParser

    argp = ArgumentParser()
    shared_opts(argp)
    textartdemo_argspec(argp)
    argx = argp.parse_args()
    print(*argx.gtor(argx), sep=argx.sep)


_ASC = r'do di re ri mi fa fi so si la li ti'
_DSC = r'do+1 ti te la le so se fa mi me re ra'
_SCALE = tuple(_ASC.split()) + tuple(_DSC.split())


def textartdemo_argspec(argp):
    argp.add_argument(r'-k', r'--key', default=r'C')
    argp.add_argument(r'nth', nargs=r'*')
    argp.set_defaults(gtor=textartdemo_argx, sep=r' ')


def textartdemo_argx(argx=None):
    if argx is None:
        from argparse import Namespace
        argx = Namespace()
        argx.nth, argx.key, argx.lyric = _SCALE, r'Cn', r'english'
    elif not argx.nth:
        argx.nth = _SCALE
    yield from textartdemo(argx.nth, argx.key, argx.lyric, argx.movable_do)


def textartdemo(nth=_SCALE, key=r'Cn', lyric=r'english', movable_do=False):
    from ..ns import Cn, NS

    key = NS[key]  # reused below. do not `yield NS[key].textart`
    yield key.textart

    for y in nth:
        y = Cn(4, y).transpose(key)  # `key` is reused here
        yield r'%s%s' % (y, y.solfege(movable_do=movable_do))
