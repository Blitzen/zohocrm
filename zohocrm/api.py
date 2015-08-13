from __future__ import unicode_literals

import requests


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

    def _params(self):
        return dict(
            scope = 'crmapi',
            authtoken = self.auth_token,
        )

    def _request(self, path, format='json', method='get'):
        root_path = self.json_root_path if format == 'json' else self.xml_root_path

        url = '{}://{}/{}/{}'.format(
            self.protocol,
            self.domain,
            root_path,
            path
        )

        resp = self.session.get(
            url,
            params = self._params()
        )

        return self._handle_response(resp)

    def _handle_response(self, response):
        return response.json()['response']['result']


