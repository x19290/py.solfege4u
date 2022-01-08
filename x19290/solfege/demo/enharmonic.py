# Copyright (C) 2021 Hiroki Horiuchi <x19290@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.


_DODIRARE = r'do di ra re'.split()


def enharmonicdemo_main():
    from . import shared_opts
    from argparse import ArgumentParser

    argp = ArgumentParser()
    enharmonicdemo_argspec(argp)
    argx = argp.parse_args()
    print(*argx.gtor(argx), sep=argx.sep)


def enharmonicdemo_argspec(argp):
    argp.add_argument(r'-k', r'--key', default=r'C')
    argp.set_defaults(gtor=enharmonicdemo_argx, sep=r'')


def enharmonicdemo_argx(argx=None):
    if argx is None:
        from argparse import Namespace
        argx = Namespace()
        argx.key, argx.lyric = r'C', r'english'
    yield from enharmonicdemo(argx.key, argx.lyric)


def enharmonicdemo(key=r'C', lyric=r'english'):
    from ..ns import C, NS
    from ..xml_templates import FIRST_ATTR, G_CLEF, HEAD, ROOT, TEMPO
    from .. import SOLFEGE_EN, SOLFEGE_IT
    from itertools import cycle
    import xml.etree.ElementTree as ET
    key = NS[key]

    sillables = dict(e=SOLFEGE_EN, i=SOLFEGE_IT, n=None)[lyric[:1]]

    signature0 = dict(
        beats=4, beat_type=4, divisions=1, clef=G_CLEF, keynumber=key.number,
    )

    root = ET.fromstring(ROOT)
    part = root.find(r'part')

    pitches = (C(4, y).transpose(key) for y in _DODIRARE)
    notes = tuple(
        y.xml(duration=1, type=r'quarter', sillables=sillables)
        for y in pitches
    )

    def measure():
        this = ET.Element(r'measure', number=r'1')
        this.append(ET.fromstring(FIRST_ATTR % signature0))
        this.append(ET.fromstring(TEMPO % dict(tempo=80)))
        for y in notes:
            this.append(y)
        return this

    part.append(measure())
    
    yield HEAD
    ET.indent(root, r'    ')  # TODO: not works without the fix. no idea
    yield ET.tostring(root, encoding=r'unicode')
