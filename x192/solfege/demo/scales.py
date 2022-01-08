# Copyright (C) 2021 Hiroki Horiuchi <x19290@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.


def scalesdemo_main():
    from . import shared_opts
    from argparse import ArgumentParser

    argp = ArgumentParser()
    shared_opts(argp)
    scalesdemo_argspec(argp)
    argx = argp.parse_args()
    print(*argx.gtor(argx), sep=argx.sep)


def scalesdemo_argspec(argp):
    from ...lib.argchoices import arg_choices
    argp.add_argument(r'-t', r'--tempo', default=80, type=int)
    argp.add_argument(r'-l', r'--length', **arg_choices(r'quarter half full'))
    argp.set_defaults(gtor=scalesdemo_argx, sep=r'')


def scalesdemo_argx(argx=None):
    if argx is None:
        from argparse import Namespace
        argx = Namespace()
        argx.lyric, argx.tempo, argx.length = r'english', 80, r'quater'

    length = dict(q=1, h=2, f=4)[argx.length[:1]]
    yield from scalesdemo(argx.tempo, length, argx.lyric)


def scalesdemo(tempo=80, length=1, lyric=r'english'):
    from ..ns import C, P, Q, R, S
    from ..xml_templates import ATTR, FIRST_ATTR, G_CLEF, HEAD, ROOT, TEMPO
    from .. import SOLFEGE_EN, SOLFEGE_IT
    from itertools import count, cycle
    import xml.etree.ElementTree as ET

    sillables = dict(e=SOLFEGE_EN, i=SOLFEGE_IT, n=None)[lyric[:1]]

    signature0 = dict(
        beats=12, beat_type=8, divisions=2, clef=G_CLEF, keynumber=0,
    )

    root = ET.fromstring(ROOT)
    part = root.find(r'part')

    def c(dodireri):
        return C(4, dodireri)

    asc = (
        c(r'do'), c(r'di'), c(r're'), c(r'ri'),
        c(r'mi'),
        c(r'fa'), c(r'fi'), c(r'so'), c(r'si'), c(r'la'), c(r'li'),
        c(r'ti'),
    )
    dsc = (
        c(r'do+1'),
        c(r'ti'), c(r'te'), c(r'la'), c(r'le'), c(r'so'), c(r'se'),
        c(r'fa'),
        c(r'mi'), c(r'me'), c(r're'), c(r'ra'),
    )
    asc_dsc = asc + dsc

    def keys():
        from .. import PERFECT5TH_SEMITONES

        for hour in (P, Q, R, S)[:length]:
            # transpose by perfect 5th, perfect 5th,...
            for y in range(0, PERFECT5TH_SEMITONES * 12, PERFECT5TH_SEMITONES):
                yield hour(y % 12) + C
    keys = tuple(keys())

    def pitches():
        for key in keys:
            yield from(pitch.transpose(key) for pitch in asc_dsc)
    pitches = tuple(pitches())

    def notes():
        beams = cycle(r'begin continue continue end'.split())
        for beam, y in zip(beams, pitches):
            xmlnode = y.xml(
                duration=1, type=r'eighth', beam=beam, sillables=sillables
            )
            yield xmlnode
    notes = tuple(notes())
    notes = cycle(notes)

    keynumber_gen = (y.number for y in keys)
    keynumber_gen.__next__()

    def measure(number):
        this = ET.Element(r'measure', number=number.__str__())
        if number == 1:
            this.append(ET.fromstring(FIRST_ATTR % signature0))
            this.append(ET.fromstring(TEMPO % dict(tempo=tempo)))
        else:
            this.append(ET.fromstring(r'<print new-system="yes" />'))
            if number % 2 == 1:
                this.append(ET.fromstring(ATTR % keynumber_gen.__next__()))
        for _ in range(12):
            this.append(notes.__next__())
        return this

    try:
        for number in count(1):
            part.append(measure(number))
    except StopIteration:
        pass

    yield HEAD
    ET.indent(root, r'    ')
    yield ET.tostring(root, encoding=r'unicode')
