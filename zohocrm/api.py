from __future__ import unicode_literals
from xml.etree import ElementTree

import requests


class ZohoCRMAPIError(Exception):
    pass


record_types = (
    'leads',
    'contacts',
)


xml_template = '''<{record_name}>
{rows}
</{record_name}>'''


row_template = '''<row no="{row_number}">
{values}</row>'''

value_template = '<FL val="{key}"><![CDATA[{value}]]></FL>\n'


def records_to_xml(records):
    '''
    Given a dict of records create xml.

    format expected is:
    {
        'leads': [{ 'Company': 'Some Company, ... }, ...]
    }
    '''
    global record_types
    xml_records = ''

    for record_type in record_types:
        if record_type not in records:
            continue
        data = records[record_type]
        if not isinstance(data, list):
            data = [data]
        rows = ''
        for i, row in enumerate(data):
            values = ''
            for key in row:
                values += value_template.format(
                    key=key,
                    value=row[key],
                )
            rows += row_template.format(
                row_number = i + 1,
                values = values,
            )
        xml_records += xml_template.format(
            record_name = record_type.title(),
            rows = rows,
        )
    return xml_records


def get_auth_token(email, password):
    #https://accounts.zoho.com/apiauthtoken/nb/create?SCOPE=ZohoCRM/crmapi&EMAIL_ID=albert%2Bzohocrm%40albertoconnor.ca&PASSWORD=qw300w%3A%29
    url = 'https://accounts.zoho.com/apiauthtoken/nb/create'
    params = dict(
        SCOPE = 'ZohoCRM/crmapi',
        EMAIL_ID = email,
        PASSWORD = password,
    )

    resp = requests.get(
        url,
        params = params
    )

    auth_token = None

    # TODO: This parse isn't very robust,
    # but neither is zoho's response format
    for line in resp.text.split('\n'):
        if line.startswith('RESULT'):
            key,value = line.split('=')
            if value == 'TRUE':
                result = True
            else:
                result = False

        if line.startswith('AUTHTOKEN'):
            key,value = line.split('=')
            auth_token = value

    if result:
        return auth_token

    else:
        return False


class API(object):
    def __init__(self, auth_token, session=None):
        self.protocol = 'https'
        self.domain = 'crm.zoho.com'
        self.xml_root_path = 'crm/private/xml'
        self.json_root_path = 'crm/private/json'

        self.auth_token = auth_token
        if session is not None:
            self.session = session
        else:
            self.session = requests.Session()

    def get_records(self):
        response = self._request(
            'Leads/getRecords'
        )
        return response

    def insert_records(self, record_list):
        xml_data = records_to_xml(record_list)

        if xml_data == '':
            raise ValueError(
                'Unable to create xml from record_list:\n{}'.format(record_list)
            )

        response = self._request(
            'Leads/insertRecords',
            format = 'xml',
            method = 'post',
            params = dict(
                xmlData = xml_data,
            )
        )
        return response

    def _update_params(self, params=None):
        if params is None:
            params = dict()

        defaults = dict(
            scope = 'crmapi',
            authtoken = self.auth_token,
        )

        defaults.update(params)
        return defaults

    def _request(self, path, format='json', method='get', params=None):
        root_path = self.json_root_path if format == 'json' else self.xml_root_path

        url = '{}://{}/{}/{}'.format(
            self.protocol,
            self.domain,
            root_path,
            path
        )

        if method == 'get':
            func = self.session.get
        elif method == 'post':
            func = self.session.post
        else:
            raise ValueError(
                '{} isn\'t a valid method, get or post allowed'.format(method)
            )

        resp = func(
            url,
            params = self._update_params(params)
        )

        return self._handle_response(resp)

    def _handle_response(self, response):
        try:
            json = response.json()
        except ValueError:
            return self._handle_xml(response.text)

        if 'result' in json['response']:
            return json['response']['result']
        else:
            raise ZohoCRMAPIError(json)

    def _handle_xml(self, xml):
        # TODO: https://docs.python.org/2/library/xml.html#defused-packages
        # because we shouldn't true zoho
        return ElementTree.fromstring(xml)


