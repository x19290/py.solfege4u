# Copyright (C) 2021 Hiroki Horiuchi <x19290@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

def arg_choices(choices, shorten=None):
    if shorten is None:
        def shorten(g):
            yield from (y[:1] for y in g)

    def gen_choices():
        longs = tuple(choices.split())
        for short, long in zip(shorten(longs), longs):
            yield from (short, long)

    choices = tuple(gen_choices())

    return dict(
        choices=choices,
        default=choices[0],
    )