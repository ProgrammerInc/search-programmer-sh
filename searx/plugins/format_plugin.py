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

name = "Format plugin"
description = gettext("Formats strings to a specific case.")
default_on = True
preference_section = 'query'
query_keywords = ['camelcase', 'kebabcase', 'lowercase', 'pascalcase', 'snakecase', 'swapcase', 'titlecase', 'uppercase', 'camel', 'kebab', 'lower', 'pascal', 'snake', 'swap', 'title', 'upper']
query_examples = 'uppercase The quick brown fox jumps over the lazy dog'

parser_re = re.compile('(camelcase|kebabcase|lowercase|pascalcase|snakecase|swapcase|titlecase|uppercase|camel|kebab|lower|pascal|snake|swap|title|upper) (.*)', re.I)

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

    # format camelcase string
    # Source: https://www.30secondsofcode.org/python/s/camel
    if function == 'camel' or function == 'camelcase':
        new_string = re.sub(r"(_|-)+", " ", string).title().replace(" ", "")
        camelcased_string = ''.join([new_string[0].lower(), new_string[1:]])
        answer = gettext('Camelcased string') + ": " + camelcased_string

    # format kebabcase string
    # Source: https://www.30secondsofcode.org/python/s/kebab
    if function == 'kebab' or function == 'kebabcase':
        kebabcased_string = '-'.join(
            re.sub(r"(\s|_|-)+"," ",
            re.sub(r"[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+",
            lambda mo: ' ' + mo.group(0).lower(), string)).split()
        )
        answer = gettext('Kebabcased string') + ": " + kebabcased_string

    # format lowercase string
    if function == 'lower' or function == 'lowercase':
        lowercased_string = string.lower()
        answer = gettext('Lowercased string') + ": " + lowercased_string

    # format pascalcase string
    # Source: https://www.geeksforgeeks.org/python-convert-snake-case-to-pascal-case/
    if function == 'pascal' or function == 'pascalcase':
        pascalcased_string = string.replace("_", " ").title().replace(" ", "")
        answer = gettext('Pascalcased string') + ": " + pascalcased_string
    
    # format snakecase string
    # Source: https://www.30secondsofcode.org/python/s/snake
    if function == 'snake' or function == 'snakecase':
        snakecased_string = '_'.join(
            re.sub('([A-Z][a-z]+)', r' \1',
            re.sub('([A-Z]+)', r' \1',
            string.replace('-', ' '))).split()).lower()
        answer = gettext('Snakecased string') + ": " + snakecased_string
    
    # format swapcase string
    if function == 'swap' or function == 'swapcase':
        swapcased_string = string.swapcase()
        answer = gettext('Swapcased string') + ": " + swapcased_string

    # format titlecase string
    if function == 'title' or function == 'titlecase':
        titlecased_string = string.title()
        answer = gettext('Titlecased string') + ": " + titlecased_string

    # format uppercase string
    if function == 'upper' or function == 'uppercase':
        uppercased_string = string.upper()
        answer = gettext('Uppercased string') + ": " + uppercased_string

    # print result
    search.result_container.answers.clear()
    search.result_container.answers['format'] = {'answer': answer}
    return True
