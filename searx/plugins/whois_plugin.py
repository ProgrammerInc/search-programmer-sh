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
import datetime
import whois
import re

name = "WHOIS Lookup plugin"
description = gettext("Displays WHOIS information for a given hostname or IP address.")
default_on = True
preference_section = 'query'
query_keywords = ['whois']
query_examples = 'whois programmer.sh'

parser_re = re.compile('(whois) (.*)', re.I)

# Source: https://www.thepythoncode.com/article/extracting-domain-name-information-in-python

def is_registered(domain_name):
    """
    A function that returns a boolean indicating 
    whether a `domain_name` is registered
    """
    try:
        w = whois.whois(domain_name)
    except Exception:
        return False
    else:
        return bool(w.domain_name)

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

    # display WHOIS information
    if function == 'whois' and is_registered(string):
        whois_info = whois.whois(string)

        if whois_info.domain_name:
            answer += gettext('Domain Name') + ": " + (whois_info.domain_name[0], whois_info.domain_name)[isinstance(whois_info.domain_name, str)] + "\n"

        if whois_info.registrar:
            answer += gettext('Registrar') + ": " + (whois_info.registrar[0], whois_info.registrar)[isinstance(whois_info.registrar, str)] + "\n"

        if whois_info.referral_url:
            answer += gettext('Referral URL') + ": " + (whois_info.referral_url[0], whois_info.referral_url)[isinstance(whois_info.referral_url, str)] + "\n"

        if whois_info.whois_server:
            answer += gettext('WHOIS Server') + ": " + (whois_info.whois_server[0], whois_info.whois_server)[isinstance(whois_info.whois_server, str)] + "\n"

        if whois_info.creation_date:
            if isinstance(whois_info.creation_date, datetime.datetime):
                answer += gettext('Creation Date') + ": " + whois_info.creation_date.isoformat() + "\n"
            else:
                answer += gettext('Creation Date') + ": " + whois_info.creation_date[0].isoformat() + "\n"
        
        if whois_info.updated_date:
            if isinstance(whois_info.updated_date, datetime.datetime):
                answer += gettext('Updated Date') + ": " + whois_info.updated_date.isoformat() + "\n"
            else:
                answer += gettext('Updated Date') + ": " + whois_info.updated_date[0].isoformat() + "\n"

        if whois_info.expiration_date:
            if isinstance(whois_info.expiration_date, datetime.datetime):
                answer += gettext('Expiration Date') + ": " + whois_info.expiration_date.isoformat() + "\n"
            else:
                answer += gettext('Expiration Date') + ": " + whois_info.expiration_date[0].isoformat() + "\n"

        if whois_info.name_servers:
            answer += gettext('Nameservers') + ": \n" + ("\n ".join(whois_info.name_servers), whois_info.name_servers)[isinstance(whois_info.name_servers, str)] + "\n"

        if whois_info.dnssec:
            answer += gettext('DNSSEC') + ": " + (", ".join(whois_info.dnssec), whois_info.dnssec)[isinstance(whois_info.dnssec, str)] + "\n"

        if whois_info.org:
            answer += gettext('Organization') + ": " + (whois_info.org[0], whois_info.org)[isinstance(whois_info.org, str)] + "\n"

        if whois_info.name:
            answer += gettext('Name') + ": " + (whois_info.name[0], whois_info.name)[isinstance(whois_info.name, str)] + "\n"

        if whois_info.emails:
            answer += gettext('Emails') + ": " + ("\n ".join(whois_info.emails), whois_info.emails)[isinstance(whois_info.emails, str)] + "\n"

        if whois_info.address:
            answer += gettext('Address') + ": " + (whois_info.address[0], whois_info.address)[isinstance(whois_info.address, str)] + "\n"

        if whois_info.city:
            answer += gettext('City') + ": " + (whois_info.city[0], whois_info.city)[isinstance(whois_info.city, str)] + "\n"

        if whois_info.state:
            answer += gettext('State') + ": " + (whois_info.state[0], whois_info.state)[isinstance(whois_info.state, str)] + "\n"

        if whois_info.country:
            answer += gettext('Country') + ": " + (whois_info.country[0], whois_info.country)[isinstance(whois_info.country, str)] + "\n"

        if whois_info.registrant_postal_code:
            answer += gettext('Postal Code') + ": " + (whois_info.registrant_postal_code[0], whois_info.registrant_postal_code)[isinstance(whois_info.registrant_postal_code, str)] + "\n"

        if whois_info.status:
            answer += gettext('Status') + ": \n" + ("\n ".join(whois_info.status), whois_info.status)[isinstance(whois_info.status, str)] + "\n"
        
    # print result
    search.result_container.answers.clear()
    search.result_container.answers['whois'] = {'answer': answer}
    return True
