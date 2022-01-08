# Copyright (C) 2021 Hiroki Horiuchi <x19290@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.


class RingMixin:
    divisor = 0

    def __init__(self, *_, **__):
        self.divisor = self.__len__()

    def __getitem__(self, ik):
        if isinstance(ik, int):
            rv = super(RingMixin, self).__getitem__(ik % self.divisor)
        else:
            rv = self._resolve(ik) % self.divisor
        return rv
