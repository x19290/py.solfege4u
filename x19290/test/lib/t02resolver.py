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
from ...lib.resolver import Resolver, StrResolver

_RES = Resolver(tuple(r'abc'))
_S_RES = StrResolver(r'abc')
_RES2 = Resolver(r'a,b,c')


class T0(TestCase):
    def _test(self, resolver):
        expected = 1, r'b'
        actual = tuple(resolver[y] for y in (r'b', 1))
        self.assertEqual(expected, actual)

    def test0(self):
        self._test(_RES)

    def test1(self):
        self._test(_S_RES)

    def test2(self):
        self._test(_RES2)


class T1(TestCase):
    def test0(self):
        self.assertTrue(isinstance(_RES2, tuple))