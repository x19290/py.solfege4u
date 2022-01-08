# Copyright (C) 2021 Hiroki Horiuchi <x19290@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.


def dai4demo_main():
    from . import shared_opts
    from argparse import ArgumentParser

    argp = ArgumentParser()
    shared_opts(argp)
    dai4demo_argspec(argp)
    argx = argp.parse_args()
    print(*argx.gtor(argx), sep=argx.sep)


def dai4demo_argspec(argp):
    argp.add_argument(r'-k', r'--key', default=r'Cs', help=r'default: "Cs"')
    argp.add_argument(
        r'nth', nargs=r'*',
        help=r'in movable-dodire. may be auto-repeated. default: "di"',
    )
    argp.set_defaults(gtor=dai4demo_argx, sep=r'')


def dai4demo_argx(argx=None):
    if argx is None:
        from argparse import Namespace
        argx = Namespace()
        argx.nth, argx.key, argx.lyric = (r'di',), r'Cs', r'english'
    elif not argx.nth:
        argx.nth = r'di',
    yield from dai4demo(argx.nth, argx.key, argx.lyric)


def dai4demo(nth=('di',), key=r'Cs', lyric=r'english'):
    from ..ns import C, NS
    from ..xml_templates import FIRST_ATTR, G_CLEF, HEAD, ROOT, TEMPO
    from .. import SOLFEGE_EN, SOLFEGE_IT
    from itertools import cycle
    import xml.etree.ElementTree as ET
    key = NS[key]

    sillables = dict(e=SOLFEGE_EN, i=SOLFEGE_IT, n=None)[lyric[:1]]

    signature0 = dict(
        beats=2, beat_type=4, divisions=1, clef=G_CLEF, keynumber=key.number,
    )

    root = ET.fromstring(ROOT)
    part = root.find(r'part')

    nth = (C(4, y).transpose(key) for y in nth)
    notes = tuple(
        y.xml(duration=1, type=r'quarter', sillables=sillables)
        for y in nth
    )
    notes = cycle(notes)

    def measure(number):
        this = ET.Element(r'measure', number=number.__str__())
        if number == 1:
            this.append(ET.fromstring(FIRST_ATTR % signature0))
            this.append(ET.fromstring(TEMPO % dict(tempo=80)))
        for _ in range(2):
            this.append(notes.__next__())
        return this

    try:
        for number in range(1, 3):
            part.append(measure(number))
    except StopIteration:
        pass

    yield HEAD
    root = ET.fromstring(ET.tostring(root, encoding=r'unicode')) # dirty fix
    ET.indent(root, r'    ')  # TODO: not works without the fix. no idea
    yield ET.tostring(root, encoding=r'unicode')
