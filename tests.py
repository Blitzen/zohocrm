from betamax import Betamax
from requests import Session
from unittest import TestCase, main

from zohocrm import api


with Betamax.configure() as config:
    config.cassette_library_dir = 'cassettes'


class ZohoAPITestCase(TestCase):
    def setUp(self):
        self.session = Session()
        self.invalid_api = api.API(auth_token='INVALID_TOKEN')
        self.api = api.API(auth_token='597a7029c4ea163c7a3ffeed2816c7a2', session=self.session)
        self.record = {
            'Lead Source': 'Web Download',
            'Company': 'Your Company',
            'First Name': 'Hannah',
            'Last Name': 'Smith',
            'Email': 'testing@testing.com',
            'Title': 'Manager',
            'Phone': '1234567890',
            'Home Phone': '0987654321',
        }
        self.control = '''<Leads>
<row no="1">
<FL val="First Name"><![CDATA[Hannah]]></FL>
<FL val="Title"><![CDATA[Manager]]></FL>
<FL val="Last Name"><![CDATA[Smith]]></FL>
<FL val="Phone"><![CDATA[1234567890]]></FL>
<FL val="Company"><![CDATA[Your Company]]></FL>
<FL val="Email"><![CDATA[testing@testing.com]]></FL>
<FL val="Lead Source"><![CDATA[Web Download]]></FL>
<FL val="Home Phone"><![CDATA[0987654321]]></FL>
</row>
</Leads>'''

    def test_records_to_xml(self):
        records = dict(
            leads = [self.record]
        )
        xml = api.records_to_xml(records)
        self.assertEqual(xml, self.control)

    def test_records_to_xml_no_list(self):
        records = dict(
            leads = self.record
        )
        xml = api.records_to_xml(records)
        self.assertEqual(xml, self.control)

    def test_records_to_xml_empty_unknown_key(self):
        records = dict(
            unknow_key = [self.record]
        )
        xml = api.records_to_xml(records)
        self.assertEqual(xml, '')

    def test_api_get_records_invalid(self):
        with Betamax(self.session).use_cassette('get_records_invalid'):
            with self.assertRaises(api.ZohoCRMAPIError):
                ret = self.invalid_api.get_records()

    def test_api_get_records(self):
        with Betamax(self.session).use_cassette('get_records'):
            ret = self.api.get_records()
            self.assertTrue('Leads' in ret)

    def test_api_insert_records_raise_value_error(self):
        records = dict(
            unknow_key = [self.record]
        )
        with self.assertRaises(ValueError):
            self.invalid_api.insert_records(records)

    def test_api_insert_records(self):
        with Betamax(self.session).use_cassette('insert_records'):
            records = dict(
                leads = [self.record]
            )
            ret = self.api.insert_records(records)


if __name__ == '__main__':
    main()
