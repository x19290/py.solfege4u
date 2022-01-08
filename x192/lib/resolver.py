# Copyright (C) 2021 Hiroki Horiuchi <x19290@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from .centered import CenteredMixin


class ResolveMixin:
    def __new__(cls, linear):
        if r',' in linear:
            linear = linear.split(r',')
        return super(ResolveMixin, cls).__new__(cls, linear)

    def __init__(self, *_, **__):
        self.hash = {k: v for v, k in enumerate(self)}

    def __getitem__(self, ik):
        try:
            return self._indexed(ik)
        except TypeError:
            return self._hashed(ik)

    def _indexed(self, i):
        return super(ResolveMixin, self).__getitem__(i)

    def _hashed(self, k):
        return self.hash[k]


class StrResolver(ResolveMixin, str):
    pass


class Resolver(ResolveMixin, tuple):
    pass


class CenteredResolveMixin(CenteredMixin, ResolveMixin):
    def __getitem__(self, ik):
        try:
            return super(CenteredMixin, self)._indexed(ik + self.center)
        except TypeError:
            return super(CenteredMixin, self)._hashed(ik) - self.center


class CenteredStrResolver(CenteredResolveMixin, str):
    pass


class CenteredResolver(CenteredResolveMixin, tuple):
    pass