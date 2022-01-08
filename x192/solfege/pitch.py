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
A system called "Pitch System" by me -- the heart of "Solfege 192"

- keys (C, Cs=C♯,...) are subclasses of Pitch
- C.__name__ == 'C'
- Cs.__name__ = 'C♯'
- C is Cn is NS['C'] is NS['Cn']
- Cs is NS['Cs'] is NS['C♯']
- each pitch is an instance of a key
  csharp4_in_c = C(octave=4, nth=0, semitone=1)
  csharp4_in_c = C(octave=4, nth='di')
  csharp4_in_g = G(octave=4, nth=3, semitone=1)
  csharp4_in_g = G(octave=4, nth='fi')
  csharp4_in_c != csharp4_in_g
  csharp4_in_c.__str__() == 'C♯4'
  csharp4_in_g.__str__() == 'C♯4'
  csharp4_in_c.solfege(sillables=SOLFEGE_IT) == 'Di'
  csharp4_in_g.solfege(sillables=SOLFEGE_IT) == 'Di'
  csharp4_in_c.solfege() == 'Dee'
  csharp4_in_g.solfege() == 'Dee'
  csharp4_in_c.solfege(movable_do=True) == 'di'
  csharp4_in_g.solfege(movable_do=True) == 'fi'

  csharp4_in_c.xml(duration=1, type='quarter',...)
    == '<note>...</note>' (en element of MusicXML)
'''

from . import OCT_7, DODIRERI_EN, DODIRERI_IT, SOLFEGE_EN
from ..lib.centered import Centered
from ..lib.protecteddict import ProtectedDict
from ..lib.resolver import CenteredResolver, CenteredStrResolver

_MODE_FULLNAMES = r'''
Ⅰ Ionian
Ⅱ Dorian
Ⅲ Phrygian
Ⅳ Lydian
Ⅴ Mixolydian
Ⅵ Aeolian
Ⅶ Locrian
'''[1:]

FQ_MODESTRS = tuple(r'_%d' % y for y in range(1, 8))
MODESTRS = (r'',) + FQ_MODESTRS[1:]

_KEY_SIGNATURES = r'''
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

_ACCIDENTAL_RESOLVERS = Centered((
    {
        r'𝄫': -1,
        r'': 0,
        r'♮': +1,
    },
    {
	    r'♭': -1,
        r'': 0,
        r'♯': +1,
    },
    {
        r'♮': -1,
        r'': 0,
        r'𝄪': +1,
    },
))

SEMITONE = CenteredResolver(r'♭,,♯')
ACCIDENTAL = CenteredStrResolver(r'𝄫♭♮♯𝄪')
ACCIDENTAL2XML = ProtectedDict(
    **{
        r'𝄫': r'flat-flat',
        r'♭': r'flat',
        r'♮': r'natural',
        r'♯': r'sharp',
        r'𝄪': r'sharp-sharp',
    }
)
ACCIDENTAL2SAFECHAR = ProtectedDict(
    **{
        r'♭': r'f',
        r'': r'n',
        r'♯': r's',
    },
)
ACCIDENTAL_SELECTORS = Centered(f'𝄫♮,♭♯,♮𝄪')
ACCIDENTAL_RESOLVERS = Centered(map(ProtectedDict, _ACCIDENTAL_RESOLVERS))


def __pitch_parser():
    from re import compile

    return compile(r'([A-Ga-g])([𝄫♭♮♯𝄪]?)(-?\d+)')


PITCH_PARSER = __pitch_parser()

_ACCIDENTAL = r'''
    <accidental>%s</accidental>
'''[:-1]

_NOTE = r'''
<note>
    <pitch>
        <step>%(step)s</step>%(alter)s
        <octave>%(octave)s</octave>
    </pitch>
    <duration>%(duration)d</duration>
    <voice>%(voice)d</voice>
    <type>%(type)s</type>%(accidental)s%(beam)s%(lyric)s
</note>
'''[1:]

_BEAM = r'''
    <beam number="%(beam_num)d">%(beam)s</beam>
'''[:-1]

_ALTER = r'''
        <alter>%d</alter>
'''[:-1]

_LYRIC = r'''
    <lyric number="1">
        <syllabic>single</syllabic>
        <text>%s</text>
    </lyric>
'''[:-1]


class Pitch(tuple):
    @classmethod
    def parse(cls, name: str):
        alpha, accidental, octave = PITCH_PARSER.match(name).groups()
        nth = cls.resolve(alpha)
        accres = _ACCIDENTAL_RESOLVERS[cls.signature[nth]]
        return cls(int(octave), nth, accres[accidental])

    @classmethod
    def resolve(cls, alpha):
        r'''
        classmethod! diatonic!
        '''
        from . import CDEFGAB

        return (CDEFGAB[alpha] - cls.do) % OCT_7

    def __new__(cls, octave, nth, semitone=0):
        r'''
        nth: 0~6 OR do,di,re,ri,...ti,te,la,...ra
        '''
        from . import OCT_7

        if isinstance(nth, str):
            assert semitone == 0
            octave_adj = nth[2:]
            if octave_adj:
                octave += int(octave_adj)
                nth = nth[:2]
            nth, semitone = DODIRERI_IT[nth.lower()]
        div, nth = nth // OCT_7, nth % OCT_7
        octave += div
        return super(Pitch, cls).__new__(cls, (octave, nth, semitone))

    def homogenize(self):
        from .semitone import basic_semitones

        clazz = self.__class__
        start = basic_semitones(clazz.do, clazz.semitone)
        octave, nth, semitone = self
        return start + 12 * octave + basic_semitones(nth, semitone)

    @classmethod
    def class_duodecimal(cls):
        from . import PERFECT5TH_SEMITONES

        return (cls.number * PERFECT5TH_SEMITONES) % 12

    def __eq__(self, another):
        return isinstance(another, self.__class__) and\
            super(Pitch, self).__eq__(another)

    def __ne__(self, another):
        return not self.__eq__(another)

    def __hash__(self):
        return super(Pitch, self).__hash__()

    def __str__(self):
        return r'%s%s%d' % self.render()

    def render(self):
        from . import CDEFGAB

        clazz = self.__class__
        octave, nth, semitone = self
        if semitone == 0:
            accidental = r''
        else:
            stor = ACCIDENTAL_SELECTORS[clazz.signature[nth]]
            accidental = stor[semitone == 1]
        alpha = CDEFGAB[self.do + nth]
        return alpha, accidental, octave

    def transpose(self, to, octave=0):
        # TODO: test
        if to is self.__class__ and octave == 0:
            rv = self
        else:
            self_octave, nth, semitone = self
            if isinstance(to, int):
                octave += (to + octave)
                to = self.__class__
            else:
                from . import OCT_7
                octave += (to.do + nth) // OCT_7
            rv = to(self_octave + octave, nth, semitone)
        return rv

    def xml(
        self, duration, type, movable_do=False,
        voice=1, beam=None, beam_num=1, sillables=SOLFEGE_EN, postprocess=None,
    ):
        if postprocess is None:
            from xml.etree.ElementTree import fromstring as postprocess
        elif postprocess is False:
            def postprocess(xml):
                return xml

        octave, nth, semitone, s, step, suffix, base_shift = self._reparse()
        alter = base_shift + semitone
        if suffix.isdigit():
            accidental_char = r'♮'
            accidental = r''
        else:
            accidental_char = s[1:2]
            accidental = _ACCIDENTAL % ACCIDENTAL2XML[accidental_char]
        if alter == 0:
            alter = r''
        else:
            alter = _ALTER % alter
        lyric = self._solfege(
            s, nth, semitone, movable_do, base_shift,
            ACCIDENTAL[accidental_char], sillables, xml=True,
        )
        if beam is None:
            beam = r''
        else:
            beam = _BEAM % locals()
        # to avoid "not used" warnings
        accidental, beam, beam_num, duration, lyric, octave, step, type, voice
        xml = _NOTE % locals()
        return postprocess(xml)

    def solfege(self, movable_do=False, sillables=SOLFEGE_EN, xml=False):
        _octave, nth, semitone, s, _step, suffix, base_shift = self._reparse()
        if suffix.isdigit():
            accidental = 0
        else:
            accidental = ACCIDENTAL[s[1:2]]
        return self._solfege(
            s, nth, semitone, movable_do, base_shift, accidental,
            sillables, xml,
        )

    def _solfege(
        self, s, nth, semitone, movable_do, base_shift, accidental: int,
        sillables, xml=False,
    ):
        if sillables is None:
            rv = r''
        else:
            if movable_do:
                dodireri = DODIRERI_EN if sillables is SOLFEGE_EN else DODIRERI_IT
                text = dodireri[(nth, semitone)]
            else:
                from . import CDEFGAB
                nth = CDEFGAB[s[:1]]  # nothing to do with prev `nth`. confusing
                if base_shift:
                    accidental = semitone + base_shift  # prev val discarded
                text = sillables[nth][accidental]
            if xml:
                rv = _LYRIC % text
            else:
                rv = text
        return rv

    def _reparse(self):
        octave, nth, semitone = self
        s = self.__str__()
        step, suffix = s[:1], s[1:]
        base_shift = self.signature[nth]
        return octave, nth, semitone, s, step, suffix, base_shift

    def enharmonic(self, another):
        return isinstance(another, self.__class__) and\
            self.homogenize() == another.homogenize()

    @classmethod
    def class_enharmonic(cls, another):
        return issubclass(another, Pitch) and\
            cls.class_duodecimal() == another.class_duodecimal()


def __key_signatures():
    hash = ProtectedDict()
    mutable = hash.mutable

    def parse_key_signatures():
        for y in _KEY_SIGNATURES.splitlines(keepends=False):
            keyname, textart = y.split()
            signature = tuple(ACCIDENTAL[y]for y in textart)
            mutable[keyname] = signature, sum(signature), textart
            yield keyname

    names = tuple(parse_key_signatures())
    assert mutable.__len__() == 7 + 1 + 7
    yield from (names, hash)


KEY_NAMES, KEY_SIGNATURES = __key_signatures()
