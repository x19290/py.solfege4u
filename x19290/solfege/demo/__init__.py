# Copyright (C) 2021 Hiroki Horiuchi <x19290@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

__date__, __updated__ = r'2021-06', r'2021-07'
__author__ = r'x19290@gmail.com'


def __strconsts():
    def name(sep):
        from pathlib import Path
        from re import compile
        from sys import argv

        sep_cre = compile(sep)
        fix = (lambda y: y.title()) if sep == r' ' else (lambda y: y)
        return sep.join(fix(y) for y in sep_cre.split(Path(argv[0]).stem))

    natural_progname, progname = map(name, (r' ', r'-'))
    revision = r'v0.01'
    author = __author__[:__author__.index(r'@')]
    identity = r'https://github.com/%s/py.solfege4u.git' % author

    yield from (natural_progname, progname, revision, identity)


NATURAL_PROGNAME, PROGNAME, REVISION, IDENTITY = __strconsts()

_LYRICS = r'english italian none'


def shared_opts(argp):
    from ...lib.argchoices import arg_choices

    argp.add_argument(r'-l', r'--lyric', **arg_choices(_LYRICS))
    argp.add_argument(r'-m', r'--movable-do', action=r'store_true')
