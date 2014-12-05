#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch
from concurrent import futures
import json
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
from tornado.httpclient import HTTPError, HTTPResponse, HTTPRequest
from io import BytesIO
import tests.utils
from luiza_labs.handlers import api
from luiza_labs.business.model import PersonModel


class TestApi(AsyncHTTPTestCase):
    def setUp(self):
        super(TestApi, self).setUp()
        self.database = tests.utils.make_mock_database_connection()

    def tearDown(self):
        tests.utils.clear_mock_database(self.database)
        super(TestApi, self).tearDown()

    def get_app(self):
        return Application([(r"/person/", api.PersonHandler),
                            (r"/person/([^/]+)/", api.PersonHandler)])

    @patch('luiza_labs.handlers.api.Person.save_from_facebook')
    def test_post(self, mock_person):
        future = futures.Future()
        future.set_result(True)
        mock_person.return_value = future
        self.http_client.fetch(self.get_url('/person/'),
                               self.stop,
                               method='POST',
                               body='facebookId=123456789')
        response = self.wait()
        self.assertEqual(201, response.code)
        mock_person.assert_called_once_with('123456789')

    def test_post_without_facebook_id(self):
        self.http_client.fetch(self.get_url('/person/'),
                               self.stop,
                               method='POST',
                               body='foo=bar')
        response = self.wait()
        self.assertEqual(500, response.code)
        self.assertEqual('facebookId required', json.loads(response.body.decode())['error'])

    @patch('luiza_labs.business.person.AsyncHTTPClient')
    def test_post_person_not_found(self, mock_http_client):
        future = futures.Future()
        response = HTTPResponse(HTTPRequest(''),
                                404,
                                buffer=BytesIO(b'{"error": "Some of the aliases you requested do not exist"}'))
        exception = HTTPError(404, 'Not Found', response)
        future.set_exception(exception)
        mock_http_client.return_value.fetch.return_value = future

        self.http_client.fetch(self.get_url('/person/'),
                               self.stop,
                               method='POST',
                               body='facebookId=drgarcia1986')
        response = self.wait()
        self.assertEqual(404, response.code)
        self.assertEqual('Not Found', response.reason)

    def test_get(self):
        tests.utils.data_for_testing(self.database.session())
        self.http_client.fetch(self.get_url('/person/'),
                               self.stop)
        response = self.wait()
        self.assertEqual(200, response.code)
        list = json.loads(response.body.decode())
        self.assertTrue(len(list) == 2)

        self.http_client.fetch(self.get_url('/person/?limit=1'),
                               self.stop)
        response = self.wait()
        self.assertEqual(200, response.code)
        list = json.loads(response.body.decode())
        self.assertTrue(len(list) == 1)

        s = self.database.session()
        s.query(PersonModel).filter_by(facebook_id=list[0]['facebook_id']).delete()
        s.commit()

        self.http_client.fetch(self.get_url('/person/'),
                               self.stop)
        response = self.wait()
        self.assertEqual(200, response.code)
        list = json.loads(response.body.decode())
        self.assertTrue(len(list) == 1)

    def test_delete(self):
        tests.utils.data_for_testing(self.database.session())
        s = self.database.session()
        list = s.query(PersonModel).all()
        self.assertTrue(len(list) == 2)

        self.http_client.fetch(self.get_url('/person/bar_111222/'),
                               self.stop,
                               method='DELETE')
        response = self.wait()
        self.assertEqual(204, response.code)

        list = s.query(PersonModel).all()
        self.assertTrue(len(list) == 1)
        self.assertNotEquals('bar_111222', list[0].facebook_id)


if __name__ == '__main__':
    unittest.main()
