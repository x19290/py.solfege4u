# Copyright (C) 2021 Hiroki Horiuchi <x19290@gmail.com>

# This program is derived from https://pypi.org/project/sinsy-cli/
# by Olivier Jolly in 2021-07.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# sinsy-cli, Sinsy Command Line Interface
# Copyright (C) 2016  Olivier Jolly
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from . import logd
from pathlib import Path
from time import time as now

__date__, __updated__ = r'2021-03-14', r'2021-07-12'
__author__ = r'x19290@gmail.com'


def __strconsts():
    def name(sep):
        from sys import argv

        fix = (lambda y: y.title()) if sep == r' ' else (lambda y: y)
        return sep.join(fix(y) for y in Path(argv[0]).stem.split(r'-'))

    base_url = r'http://sinsy.sp.nitech.ac.jp/'
    natural_progname, progname = map(name, (r' ', r'-'))
    revision = r'0.9'
    author = __author__[:__author__.index(r'@')]
    identity = r'https://bitbucket.org/%s/%s.git' % (author, progname)
    user_agent = r'%s/%s (+%s)' % (natural_progname, revision, identity)

    yield from (base_url, user_agent, progname, revision)


_BASE_URL, _USER_AGENT, PROGNAME, REVISION = __strconsts()
LANGUAGES = r'english japanese chinese'

_INDEX_PHP = _BASE_URL + r'index.php'
_HEADERS = {r'User-Agent': _USER_AGENT}


class LangError(ValueError):
    pass


class BankError(ValueError):
    pass


class GenderError(ValueError):
    pass


class VibratoError(ValueError):
    pass


class TransposeError(ValueError):
    pass


r'''
language: english, valid speaker: 45
language: japanese, valid speaker: 0123789,10
'''
PARAMSPEC = dict(
    debug=(None, None, r'raise log level from INFO TO DEBUG'),
    version=(None, None),
    language=(None, None, r'Vocal bank language [defaults: %(default)s]'),
    speaker=(None, None,
        (
            r'Vocal bank index for the given spoken language '
            r'[from 0, max depends on language, default: %(default)s]. '
            r'You must specify 10, 11 or 12 for --language=en. '
            r'Very bad UI that directly comes from https://sinsy.jp/'
        ),
    ),
    gender=((-0.8, 0.8), GenderError, r' parameter', r''),
    vibrato=((0.0, 2.0), VibratoError, r' intensity', r''),
    transpose=((-24, 24), TransposeError, r'', r'in semitones, '),
)

class SynthesisError(Exception):
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return r'Synthesis failed. HTTP error code %s' % self.code


class GiveUp(Exception):
    def __init__(self, *args, **kwargs):
        super(GiveUp, self).__init__(r'--debug will not help', *args, **kwargs)


def cheatweb_sinsy(
    musicxml,
    lang,
    speaker,
    gender,
    vibrato,
    transpose,
):
    r'''
    send a MusicXML to be processed by sinsy
    '''

    from bs4 import BeautifulSoup
    from requests import post as rq_post, get as rq_get

    ns = locals()
    for y in r'gender vibrato transpose'.split():
        ((lowerbound, upperbound), e, *_), y = PARAMSPEC[y], ns[y]
        if not (lowerbound <= y <= upperbound):
            raise e(y)

    request_data = dict(
        LANG=r'en',  # lang of the web-ui
        SPKR_LANG=lang,
        SPKR=speaker,
        SYNALPHA=gender,
        VIBPOWER=vibrato,
        F0SHIFT=transpose,
    )

    logd(r'{Synthesizing ...')

    with open(musicxml, r'rb') as istream:
        start = now()
        r = rq_post(
            _INDEX_PHP,
            data=request_data,
            files=dict(SYNSRC=(musicxml, istream, r'application')),
            headers=_HEADERS,
        )
        duration = now() - start

    if r.status_code == 200:
        logd(r'}Synthesis finished in %.1fs' % duration)
    else:
        raise SynthesisError(r.status_code)

    soup = BeautifulSoup(r.text, r'html.parser')
    saved = False
    for result_tag in soup.find(r'audio').parent.parent.findAll(r'a'):
        if r'wav' in result_tag.contents:
            raw_href = result_tag[r'href']
            url = _BASE_URL + raw_href[2:]
            ofile = Path(musicxml).stem
            ofile = Path(ofile + r'-sinsy.wav')
            logd(r'{Saving %s to %s' % (url, ofile))
            with ofile.open(r'wb') as ostream:
                for y in rq_get(url, headers=_HEADERS).iter_content():
                    ostream.write(y)
            logd(r'}Saved')
            saved = True
            break
    if not saved:
        raise GiveUp(r'input too long?')
