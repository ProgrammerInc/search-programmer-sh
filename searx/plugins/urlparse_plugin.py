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
import urllib.parse
import re

name = "URL Parse plugin"
description = gettext("URL encode strings and decodes URL encoded strings.")
default_on = True
preference_section = 'query'
query_keywords = ['urlencode', 'urldecode']
query_examples = 'urldecode Hell%C3%B6+W%C3%B6rld%40Python'

parser_re = re.compile('(urlencode|urldecode) (.*)', re.I)

# Source: https://www.urlencoder.io/python/

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

    # URL encode string
    if function == 'urlencode':
        encoded_string = urllib.parse.quote(string)
        answer = gettext('URL encoded string') + ": " + encoded_string
    
    # Decode URL encoded string
    if function == 'urldecode':
        decoded_string = urllib.parse.unquote(string)
        answer = gettext('Decoded URL encoded string') + ": " + decoded_string

    # print result
    search.result_container.answers.clear()
    search.result_container.answers['urlparse'] = {'answer': answer}
    return True
