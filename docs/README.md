# Solfege For You

Generates sample solfege in MusicXML and WAV.

The output is in Aaron Shearer's
[fixed-do](https://en.wikipedia.org/wiki/Solf%C3%A8ge#Chromatic_variants)
(Doh, Dee, Ray,...) by default,
or in
[movable-do](https://en.wikipedia.org/wiki/Solf%C3%A8ge#Movable_do_solf%C3%A8ge)
(doh, dee, ray,...) by `--movable-do` option.

Doh, Dee, Ray,... (--lyric=english) are for singing synthesis.
Do, Di, Re,... (--lyric=italian) are for printing.

- solfege4u_demo.py  
  demo program. generates MusicXML (or textart)

- x19290/solfege/\*.py  
  main implementations, API providers

- x19290/solfege/demo/*.py  
  plugins for `solfege4u_demo.py`

- cheatweb-sinsy  
  generates a .wav file from given .musicxml hitting
  [https://sinsy.jp/](https://sinsy.jp/)

- [9sample-outputs/](../9sample-outputs/0readme.md)  
  outputs from solfege4u_demo.py

The two commands have --help options.

Currently, the easiest way to generate your favorite solfege is
to write a demo plugin.

See [mindoc](../0mindoc.md) for more information

by [Hiroki Horiuchi <x19290@gmail.com\>](mailto:x19290@gmail.com)
