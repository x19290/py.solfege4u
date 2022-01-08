# Copyright (C) 2021 Hiroki Horiuchi <x19290@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.


class CenteredMixin:
    def __init__(self, *_, **__):
        super(CenteredMixin, self).__init__()
        self.center = self.__len__() // 2

    def __getitem__(self, i):
        return super(CenteredMixin, self).__getitem__(i + self.center)


class Centered(CenteredMixin, tuple):
    def __new__(cls, contents):
        if isinstance(contents, str) and r',' in contents:
            contents = contents.split(r',')
        return super(Centered, cls).__new__(cls, contents)


class CenteredStr(CenteredMixin, str):
    pass
