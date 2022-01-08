# Copyright (C) 2021 Hiroki Horiuchi <x19290@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

def import_file(path, modname, package=None):
    level = 0
    if modname.startswith('.'):
        if not package:
            raise TypeError
        for c in modname:
            if c != '.':
                break
            level += 1
    # return _bootstrap._gcd_import(name[level:], package, level)
    from importlib.util import spec_from_file_location, module_from_spec
    # if package is not None:
    #     ???
    spec = spec_from_file_location(modname, path)
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod