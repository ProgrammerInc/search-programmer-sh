'''
searx is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

searx is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with searx. If not, see < http://www.gnu.org/licenses/ >.

(C) 2015 by Adam Tauber, <asciimoo@gmail.com>
(C) 2018, 2020 by Vaclav Zouzalik
(C) 2022 by Programmer Inc.
'''

from flask_babel import gettext
import re

name = "Hex to RGB plugin"
description = gettext("Converts Hex to RGB and RGB to Hex.")
default_on = True
preference_section = 'query'
query_keywords = ['hex2rgb', 'rgb2hex']
query_examples = 'hex2rgb #FFA501'

parser_re = re.compile('(hex2rgb|rgb2hex) (.*)', re.I)

def post_search(request, search):
    # process only on first page
    if search.search_query.pageno > 1:
        return True
    m = parser_re.match(search.search_query.query)
    if not m:
        # wrong query
        return True

    function, string = m.groups()
    if string.strip().__len__() == 0:
        # end if the string is empty
        return True

    answer = ''

    # convert hex to rgb
    # Source: https://www.30secondsofcode.org/python/s/hex-to-rgb
    if function == 'hex2rgb':
        new_string = string.strip("#")
        if len(new_string) > 6 or not int(new_string, 16):
            return True
        hex_to_rgb = tuple(int(new_string[i:i+2], 16) for i in (0, 2, 4))
        answer = gettext('Hex to RGB') + ": (" + ', '.join(map(str, hex_to_rgb)) + ")"
    
    # convert rgb to hex
    # Source: https://www.30secondsofcode.org/python/s/rgb-to-hex
    if function == 'rgb2hex':
        rgb_values = []
        for value in string.strip("() ").split(',')[0:3]:
            try:
                rgb_values.append(int(value))
            except ValueError:
                return True
        rgb_to_hex = ('{:02X}' * 3).format(*rgb_values)
        answer = gettext('RGB to Hex') + ": #" + rgb_to_hex

    # print result
    search.result_container.answers.clear()
    search.result_container.answers['hex2rgb'] = {'answer': answer}
    return True
