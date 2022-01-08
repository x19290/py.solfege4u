# Copyright (C) 2021 Hiroki Horiuchi <x19290@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

HEAD = r'''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 3.1@@@@
Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">
'''[1:].replace(r'@@@@' '\n', r' ')

ROOT = r'''
<score-partwise version="3.1">
    <part-list>
        <score-part id="the-part">
            <part-name>the part name</part-name>
        </score-part>
    </part-list>
    <part id="the-part" />
</score-partwise>
'''[1:]

FIRST_ATTR = r'''
<attributes>
    <divisions>%(divisions)d</divisions>
    <key>
        <fifths>%(keynumber)d</fifths>
    </key>
    <time>
        <beats>%(beats)d</beats>
        <beat-type>%(beat_type)d</beat-type>
    </time>%(clef)s
</attributes>
'''[1:]

G_CLEF = r'''
<clef>
    <sign>G</sign>
    <line>2</line>
</clef>
'''[:-1]

TEMPO = r'''
<direction placement="above">
    <direction-type>
        <metronome>
            <beat-unit>quarter</beat-unit>
            <per-minute>%(tempo)d</per-minute>
        </metronome>
    </direction-type>
    <sound tempo="%(tempo)d"/>
</direction>
'''[1:]

ATTR = r'''
<attributes>
    <key>
        <fifths>%d</fifths>
    </key>
</attributes>
'''[1:]