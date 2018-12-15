#!/usr/bin/env python3

# Copyright (c) 2018 Filip Szymański. All rights reserved.
# Use of this source code is governed by an MIT license that can be
# found in the LICENSE file.

from datetime import datetime
import re
import urllib.request

from bs4 import BeautifulSoup

URL = 'https://unicodey.com/emoji-data/table.htm'
PATTERN = re.compile(r':\S+:')
HEADER = f'''# Copyright (c) {datetime.now().year} Filip Szymański. All rights reserved.
# Use of this source code is governed by an MIT license that can be
# found in the LICENSE file.

# This file is auto-generated from https://unicodey.com/emoji-data/table.htm.

'''

with urllib.request.urlopen(URL) as f:
    table = f.read().decode('utf-8')

lines = []
soup = BeautifulSoup(table, 'html.parser')
for row in soup.find('table').find_all('tr'):
    emoji = {}
    for cell in row.find_all('td'):
        if PATTERN.match(str(cell.string)):
            name = cell.string

        if str(cell.string).startswith('U+'):
            code_points = []
            for code_point in cell.string.split():
                if code_point == 'U+200D':
                    continue

                if len(code_point) == 6:
                    code_points.append(code_point.replace('U+', '\\u'))
                else:
                    code_points.append(code_point.replace('U+', '\\U000'))

            emoji[name] = ''.join(code_points)

            break

    lines.append(emoji)

with open('../rplugin/python3/deoplete/sources/emoji/data.py', 'w') as f:
    f.write(HEADER)
    f.write('EMOJI_CODES = {\n')
    for line in lines:
        for k, v in line.items():
            f.write(f"   '{k}': '{v}',\n")

    f.write('}')
