#!/usr/bin/env python3

# Copyright (C) 2021 Hiroki Horiuchi <x19290@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

_NO_WARRANTY = r'''
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
'''[1:-1]


from x19290.solfege.ns import A


def main(args=None):
    import x19290.solfege.demo as demo
    from x19290.solfege.demo import __author__, shared_opts
    from x19290.lib.importlib import import_file
    from argparse import ArgumentParser
    from pathlib import Path

    if args is None:
        from sys import argv
        args = argv[1:]

    g = Path(demo.__file__).parent.glob(r'[a-z]*.py')
    g = sorted(g, key=lambda y: y.stat().st_size)

    longdesc = r'Generate your favorite solfege from your plugin'
    license = r'GPL v3+ 2021 Hiroki Horiuchi <%s> -- ' % __author__
    license += _NO_WARRANTY

    argp = ArgumentParser(epilog=longdesc, description=license)
    shared_opts(argp)
    subparsers = argp.add_subparsers()

    for y in g:
        stem = y.stem
        mod = import_file(y, r'x19290.solfege.demo.' + stem)
        ns = mod.__dict__
        argspec = ns[stem + r'demo_argspec']
        argspec(subparsers.add_parser(stem[:1], aliases=(stem,)))

    argx = argp.parse_args(args)
    if not hasattr(argx, r'gtor'):
        argx = argp.parse_args((r'textart',))
    print(*argx.gtor(argx), sep=argx.sep)


if __name__ == r'__main__':
    main()
