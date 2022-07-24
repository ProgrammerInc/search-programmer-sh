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
import emoji
import re

name = "Emoji plugin"
description = gettext("Display emojis from strings and demojize strings with emojis.")
default_on = True
preference_section = 'query'
query_keywords = ['emoji', 'emojize', 'demoji', 'demojize']
query_examples = 'emojize Python :snake: is :thumbs_up:'

parser_re = re.compile('(emoji|emojize|demoji|demojize) (.*)', re.I)

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

    # display emojized string
    if function == 'emoji' or function == 'emojize':
        emoji_string = emoji.emojize(string, language='alias')
        answer = gettext('Emojized string') + ": " + emoji_string

    # display demojize string
    if function == 'demoji' or function == 'demojize':
        demoji_string = emoji.demojize(string)
        answer = gettext('Demojized string') + ": " + demoji_string

    # print result
    search.result_container.answers.clear()
    search.result_container.answers['emoji'] = {'answer': answer}
    return True
