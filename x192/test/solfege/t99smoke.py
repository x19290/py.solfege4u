# Copyright (C) 2021 Hiroki Horiuchi <x19290@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from unittest import TestCase
from solfege192_demo import main
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path


class T0scales(TestCase):
    def _test(self, lyric, tempo=None):
        if tempo is None:
            filename = r'%s.musicxml'
            args = r'-l%s scales --length=full'
        else:
            filename = r'%%s%d.musicxml' % tempo
            args = r'-l%%s scales --length=full -t%d' % tempo
        filename %= lyric
        args %= lyric[:1]
        expected = Path(__file__).resolve().parent.with_name(filename)
        expected = expected.read_text()
        b = StringIO()
        with redirect_stdout(b):
            main(args.split())
        actual = b.getvalue()
        self.assertEqual(expected, actual)

    def test0(self):
        self._test(r'en')

    def test1(self):
        self._test(r'it')

    def test2(self):
        self._test(r'en', 240)

    def test3(self):
        self._test(r'it', 240)


class T1dai4(TestCase):
    def test0(self):
        filename = r'dai4.musicxml'
        expected = Path(__file__).resolve().parent.with_name(filename)
        expected = expected.read_text()
        b = StringIO()
        with redirect_stdout(b):
            main(r'dai4'.split())
        actual = b.getvalue()
        self.assertEqual(expected, actual)


_TEXTART0CN = r'''
♮♮♮♮♮♮♮
C4Doh C♯4Dee D4Ray D♯4Ree E4Mee F4Fah F♯4Fee G4Soh G♯4See A4Lah A♯4Lee B4Tee
C5Doh B4Tee B♭4Tay A4Lah A♭4Lay G4Soh G♭4Say F4Fah E4Mee E♭4May D4Ray D♭4Rah
'''[1:-1].replace('\n', ' ') + '\n'

_TEXTART1GN = r'''
♮♮♮♮♮♮♯
G4Soh G♯4See A4Lah A♯4Lee B4Tee C5Doh C♯5Dee D5Ray D♯5Ree E5Mee E♯5Mah F5Fee
G5Soh F5Fee F♮5Fah E5Mee E♭5May D5Ray D♭5Rah C5Doh B4Tee B♭4Tay A4Lah A♭4Lay
'''[1:-1].replace('\n', ' ') + '\n'

_TEXTART2FN = r'''
♮♮♮♭♮♮♮
F4Fah F♯4Fee G4Soh G♯4See A4Lah B4Tay B♮4Tee C5Doh C♯5Dee D5Ray D♯5Ree E5Mee
F5Fah E5Mee E♭5May D5Ray D♭5Rah C5Doh C♭5Day B4Tay A4Lah A♭4Lay G4Soh G♭4Say
'''[1:-1].replace('\n', ' ') + '\n'

_TEXTART3CS = r'''
♯♯♯♯♯♯♯
C4Dee C𝄪4Dai D4Ree D𝄪4Rai E4Mah F4Fee F𝄪4Fai G4See G𝄪4Sai A4Lee A𝄪4Lai B4Tah
C5Dee B4Tah B♮4Tee A4Lee A♮4Lah G4See G♮4Soh F4Fee E4Mah E♮4Mee D4Ree D♮4Ray
'''[1:-1].replace('\n', ' ') + '\n'

_TEXTART4FS = r'''
♯♯♯♮♯♯♯
F4Fee F𝄪4Fai G4See G𝄪4Sai A4Lee B4Tee B♯4Tah C5Dee C𝄪5Dai D5Ree D𝄪5Rai E5Mah
F5Fee E5Mah E♮5Mee D5Ree D♮5Ray C5Dee C♮5Doh B4Tee A4Lee A♮4Lah G4See G♮4Soh
'''[1:-1].replace('\n', ' ') + '\n'

_TEXTART5CF = r'''
♭♭♭♭♭♭♭
C4Day C♮4Doh D4Rah D♮4Ray E4May F4Fay F♮4Fah G4Say G♮4Soh A4Lay A♮4Lah B4Tay
C5Day B4Tay B𝄫4Taw A4Lay A𝄫4Law G4Say G𝄫4Saw F4Fay E4May E𝄫4Maw D4Rah D𝄫4Raw
'''[1:-1].replace('\n', ' ') + '\n'

_TEXTART6MOVABLE_DO = r'''
♮♮♮♭♮♮♮
F4doh F♯4dee G4ray G♯4ree A4mee B4fah B♮4fee C5soh C♯5see D5lah D♯5lee E5tee
F5doh E5tee E♭5tay D5lah D♭5lay C5soh C♭5say B4fah A4mee A♭4may G4ray G♭4rah
'''[1:-1].replace('\n', ' ') + '\n'


class T2textart(TestCase):
    def _test(self, feed, expected):
        b = StringIO()
        with redirect_stdout(b):
            main(feed.split())
        actual = b.getvalue()
        self.assertEqual(expected, actual)

    def test0cn(self):
        self._test(r'textart -kCn', _TEXTART0CN)

    def test1gn(self):
        self._test(r'textart -kGn', _TEXTART1GN)

    def test2fn(self):
        self._test(r'textart -kFn', _TEXTART2FN)

    def test3cs(self):
        self._test(r'textart -kCs', _TEXTART3CS)

    def test4fs(self):
        self._test(r'textart -kFs', _TEXTART4FS)

    def test1cf(self):
        self._test(r'textart -kCf', _TEXTART5CF)

    def test6movable_do(self):
        self._test(r'-m textart -kF', _TEXTART6MOVABLE_DO)


class T3enharmonic(TestCase):
    def test0(self):
        # `actual` must be rendered like enharmonic-stuff.svg.
        # this is hard to test
        filename = r'enharmonic.musicxml'
        expected = Path(__file__).resolve().parent.with_name(filename)
        expected = expected.read_text()
        b = StringIO()
        with redirect_stdout(b):
            main(r'enharmonic'.split())
        actual = b.getvalue()
        self.assertEqual(expected, actual)
