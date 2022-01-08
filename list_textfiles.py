#!/usr/bin/python3

r'''
list almost all files that look like textfiles.
*.musicxml are excluded
'''


def main():
    from pathlib import Path

    def lookslike_textfile(y):
        name = y.name
        if name.endswith(r'.musicxml'):
            rv = False
        else:
            with y.open(r'rt', encoding=r'UTF-8') as istream:
                try:
                    istream.readline()
                except UnicodeDecodeError:
                    rv = False
                else:
                    rv = True
        return rv

    there = Path(__file__).resolve().parent
    here = Path.cwd()
    roots = (y for y in there.iterdir() if not y.name.startswith(r'.'))
    for root in sorted(roots):
        for y in sorted(root.glob(r'**/*')):
            if not y.is_symlink() and y.is_file() and lookslike_textfile(y):
                print(y.relative_to(here))


if __name__ == r'__main__':
    main()
