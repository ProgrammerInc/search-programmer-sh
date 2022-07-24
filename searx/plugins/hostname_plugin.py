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
import socket
import re

name = "Hostname plugin"
description = gettext("Displays the hostname for a given IP address.")
default_on = True
preference_section = 'query'
query_keywords = ['hostname', 'ip2hostname']
query_examples = 'hostname 8.8.8.8'

parser_re = re.compile('(hostname|ip2hostname) (.*)', re.I)

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
    if function == 'hostname' or function == 'ip2hostname':
        hostname = socket.gethostbyaddr(string)[0]
        answer = "\n" + gettext('Hostname') + ": " + hostname

    # print result
    search.result_container.answers.clear()
    search.result_container.answers['hostname'] = {'answer': answer}
    return True
