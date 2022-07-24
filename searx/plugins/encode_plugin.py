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
import base64
import re

name = "Encode plugin"
description = gettext("Encodes/Decodes strings in Base16/Base32/Base64/Base85/Ascii85 formats.")
default_on = True
preference_section = 'query'
query_keywords = ['base16', 'base16decode', 'b16e', 'b16d', 'base32', 'base32decode', 'b32e', 'b32d', 'base64', 'base64decode', 'b64e', 'b64d', 'base85', 'base85decode', 'b85e', 'b85d', 'ascii85', 'ascii85decode', 'a85e', 'a85d']
query_examples = 'base64 The quick brown fox jumps over the lazy dog'

parser_re = re.compile('(base16|base16decode|b16e|b16d|base32|base32decode|b32e|b32d|base64|base64decode|b64e|b64d|base85|base85decode|b85e|b85d|ascii85|ascii85decode|a85e|a85d) (.*)', re.I)

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

    # encode base16 string
    if function == 'base16' or function == 'b16e':
        string_bytes = string.encode('utf-8')
        base16_bytes = base64.b16encode(string_bytes)
        base16_string = base16_bytes.decode('utf-8')
        answer = gettext('base16 encoded string') + ": " + base16_string
    
    # decode base16 string
    if function == 'base16decode' or function == 'b16d':
        string_bytes = string.encode('utf-8')
        base16_bytes = base64.b16decode(string_bytes)
        base16_string = base16_bytes.decode('utf-8')
        answer = gettext('base16 decoded string') + ": " + base16_string

    # encode base32 string
    if function == 'base32' or function == 'b32e':
        string_bytes = string.encode('utf-8')
        base32_bytes = base64.b32encode(string_bytes)
        base32_string = base32_bytes.decode('utf-8')
        answer = gettext('base32 encoded string') + ": " + base32_string
    
    # decode base32 string
    if function == 'base32decode' or function == 'b32d':
        string_bytes = string.encode('utf-8')
        base32_bytes = base64.b32decode(string_bytes)
        base32_string = base64_bytes.decode('utf-8')
        answer = gettext('base32 decoded string') + ": " + base32_string

    # encode base64 string
    if function == 'base64' or function == 'b64e':
        string_bytes = string.encode('utf-8')
        base64_bytes = base64.b64encode(string_bytes)
        base64_string = base64_bytes.decode('utf-8')
        answer = gettext('base64 encoded string') + ": " + base64_string
    
    # decode base64 string
    if function == 'base64decode' or function == 'b64d':
        string_bytes = string.encode('utf-8')
        base64_bytes = base64.b64decode(string_bytes)
        base64_string = base64_bytes.decode('utf-8')
        answer = gettext('base64 decoded string') + ": " + base64_string

    # encode base85 string
    if function == 'base85' or function == 'b85e':
        string_bytes = string.encode('utf-8')
        base85_bytes = base64.b85encode(string_bytes)
        base85_string = base85_bytes.decode('utf-8')
        answer = gettext('base85 encoded string') + ": " + base85_string
    
    # decode base85 string
    if function == 'base85decode' or function == 'b64d':
        string_bytes = string.encode('utf-8')
        base85_bytes = base64.b85decode(string_bytes)
        base85_string = base85_bytes.decode('utf-8')
        answer = gettext('base85 decoded string') + ": " + base85_string

    # encode ascii85 string
    if function == 'ascii85' or function == 'a85e':
        string_bytes = string.encode('utf-8')
        ascii85_bytes = base64.a85encode(string_bytes)
        ascii85_string = ascii85_bytes.decode('utf-8')
        answer = gettext('ascii85 encoded string') + ": " + ascii85_string
    
    # decode ascii85 string
    if function == 'ascii85decode' or function == 'a64d':
        string_bytes = string.encode('utf-8')
        ascii85_bytes = base64.a85decode(string_bytes)
        ascii85_string = ascii85_bytes.decode('utf-8')
        answer = gettext('ascii85 decoded string') + ": " + ascii85_string

    # print result
    search.result_container.answers.clear()
    search.result_container.answers['encode'] = {'answer': answer}
    return True
