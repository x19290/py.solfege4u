# Copyright (C) 2021 Hiroki Horiuchi <x19290@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.


class RangedMixin:
    def __init__(self, *_, **__):
        super(RangedMixin, self).__init__()
        self.size = self.stop - self.start

    def __getitem__(self, i):
        i = (i - self.start) % self.size
        return super(RangedMixin, self).__getitem__(i)


class Ranged(RangedMixin, tuple):
    def __new__(cls, contents):
        if isinstance(contents, str) and r',' in contents:
            contents = contents.split(r',')
        return super(Ranged, cls).__new__(cls, contents)


class RangedStr(RangedMixin, str):
    pass
