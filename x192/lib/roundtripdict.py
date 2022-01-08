# Copyright (C) 2021 Hiroki Horiuchi <x19290@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from .protecteddict import ProtectedDict


class RoundtripDict(ProtectedDict):
    def __init__(self, **kwargs):
        super(RoundtripDict, self).__init__(**kwargs)
        self.outbound = tuple(kwargs.keys())[0].__class__
        self.roundtrip = {v: k for k, v in kwargs.items()}

    def __getitem__(self, k):
        hash = self.mutable if isinstance(k, self.outbound) else self.roundtrip
        return hash[k]
