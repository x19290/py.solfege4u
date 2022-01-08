# Copyright (C) 2021 Hiroki Horiuchi <x19290@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from unittest import TestCase
from ...solfege.ns import Cn, Cf, Bn

# TODO: more but not too many tests


class T0enharmonic(TestCase):
    def test0(self):
        ma = Cn(4, 2, 1)
        fa = Cn(4, 3, 0)
        self.assertTrue(ma.enharmonic(fa))


class T1class_enharmonic(TestCase):
    def test0(self):
        self.assertTrue(Cf.class_enharmonic(Bn))