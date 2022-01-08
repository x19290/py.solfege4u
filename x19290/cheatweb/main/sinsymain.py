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

_NO_WARRANTY = r'''
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
'''[1:-1]


def cheatweb_sinsymain():
    from ..sinsy import cheatweb_sinsy, SynthesisError
    from .. import logc, logi, logr, LOGD, LOGI

    argx = _argx()
    logc(format=r'%(message)s', level=LOGD)
    if argx.debug:
        logr.setLevel(LOGD)
    else:
        logr.setLevel(LOGI)

    exit_status = 0
    for xmlfile in argx.files:
        try:
            cheatweb_sinsy(
                xmlfile,
                argx.lang,
                argx.speaker,
                argx.gender,
                argx.vibrato,
                argx.transpose,
            )
        except SynthesisError as e:
            logi(e)
            exit_status = 1
        except ValueError as e:
            raise SystemExit(e.__repr__())
    raise SystemExit(exit_status)


def _argx():
    from argparse import ArgumentParser

    class Argx(ArgumentParser):
        def argument(self, longname, **kwargs):
            shortname = longname[0]
            if shortname.isupper():
                longname = shortname.lower() + longname[1:]
            kwargs.update(_help(longname))
            self.add_argument(r'-' + shortname, r'--' + longname, **kwargs)

        def __init__(self):
            from ..sinsy import __author__, __updated__,\
                PROGNAME, REVISION, LANGUAGES as langs
            from ...lib.argchoices import arg_choices

            build_date = r'%s' % __updated__
            version = r'%s %s (%s)' % (PROGNAME, REVISION, build_date)
            longdesc = r'Interact with https://singy.jp'
            license = r'GPL v3+ 2021 Hiroki Horiuchi <%s> -- ' % __author__
            license += _NO_WARRANTY

            super(Argx, self).__init__(epilog=longdesc, description=license)
            self.argument(r'debug', action=r'store_true')
            self.argument(r'Version', action=r'version', version=version)
            self.argument(r'language', dest=r'lang', **arg_choices(langs))
            self.argument(r'speaker', type=int, default=1)
            self.argument(r'gender', default=0.55, type=float)
            self.argument(r'vibrato', default=1.0, type=float)
            self.argument(r'transpose', default=0, type=int)
            self.add_argument(
                r'files', metavar=r'infile', help=r'input MusicXML',
                nargs=r'+',  # can be r'*' (with nullcontext(stdin)...)
            )

    return Argx().parse_args()


def _help(param):
    from ..sinsy import PARAMSPEC

    spec = PARAMSPEC[param]
    tmpl = spec[2:]
    tlen = tmpl.__len__()
    if tlen == 0:
        rv = {}
    else:
        if tlen == 1:
            help = tmpl[0]
        else:
            a, b = tmpl
            tmpl = param.title() + a + r' [%s%s]'
            tmpl %= (b, r'between %s and %s, default: %%(default)s')
            help = tmpl % tuple(spec[0])
        rv = dict(help=help)
    return rv
