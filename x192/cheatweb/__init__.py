# Copyright (C) 2021 Hiroki Horiuchi <x19290@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from logging import (
    root as logr, basicConfig as logc,
    debug as logd, error as loge, info as logi,
    DEBUG as LOGD, INFO as LOGI,
)


def callmain(your__file__):
    from importlib import import_module
    from pathlib import Path

    app = Path(your__file__).stem  # cheatweb-sinsy, for example
    hyphen = app.index(r'-')
    main = app[hyphen + 1:] + r'main'  # sinsymain
    entry = app[:hyphen] + r'_' + main  # cheatweb_sinsymain
    mod = import_module(r'.main.' + main, __package__)  # ...main.sinsymain
    mod.__dict__[entry]()