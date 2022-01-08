## Commands

There are two commands:

- solfege192_demo.py
- cheatweb-sinsy

`solfege192_demo.py` is an "args to stdout" command, do nothing destructive.

`cheatweb-sinsy` creates foo-sinsy.wav from foo.musicxml.

Documents are minimal currently, but `./COMMAND --help` may help.

Both require python3.

`solfege192_demo.py` might not work on old python3; for example,
it did not run on "debian:latest" of this writing (you may know that Debian is
notorious as a very conservative GNU/Linux).

But it may not require an extra python module.

`cheatweb-sinsy` may run on any python3,
but it requires extra `bs4` and `requests` modules.

## A usage example

```shell
$ ./solfege192_demo.py dai4 > daidaidaidai.musicxml
$ ./cheatweb-sinsy --speaker=4 --vibrato=0 daidaidaidai.musicxml
$ play daidaidaidai-sinsy.wav
$ musescore daidaidaidai.musicxml
```

## Testing

```shell
$ python3 -m unittest discover -p 't[0-9]*.py'
```

## IDE of my choice

I am using "Visual Studio Code (vscode)" from Microsoft.
Tons of plugins for it are available, and it contains many of them from first.
I like it very much.

They call vscode a kind of text editor (like ATOM), but it is almost an IDE.
Surprisingly, it's MIT licensed.

I don't think the comment "The best thing to come out of Microsoft in years!"
is exaggerated.

Under .vscode/, config files for vscode are.
I hope they work as-is.
