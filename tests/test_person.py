#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch
import json
import concurrent.futures
from io import BytesIO
from tornado import gen
from tornado.httpclient import HTTPResponse, HTTPRequest
import tornado.testing
import tests.utils
from luiza_labs.business.model import PersonModel
from luiza_labs.business.person import Person


class TestPersonBase(unittest.TestCase):
    def setUp(self):
        self.person = Person()
        self.database = tests.utils.make_mock_database_connection()

    def tearDown(self):
        tests.utils.clear_mock_database(self.database)


class TestPerson(TestPersonBase):
    def test_get(self):
        self.assertEqual([], self.person.get())
        tests.utils.data_for_testing(self.database.session())
        self.assertTrue(len(self.person.get(1)) == 1)
        self.assertTrue(len(self.person.get(2)) == 2)
        self.assertTrue(len(self.person.get()) == 2)
        self.assertEqual('foo', self.person.get(1)[0].username)

    def test_graph_to_person_model(self):
        data = {"id": "123foo456", "username": "foo", "first_name": "Foo", "last_name": "Bar", "gender": "male"}
        p = self.person.graph_to_person_model(json.dumps(data))
        self.assertEqual("Foo Bar", p.name)
        self.assertEqual("123foo456", p.facebook_id)
        self.assertEqual("foo", p.username)
        self.assertEqual("male", p.gender)

    def test_delete(self):
        tests.utils.data_for_testing(self.database.session())
        person_list = Person.get()
        self.assertTrue(len(person_list) > 0)
        for p in person_list:
            Person.delete(p.facebook_id)
        self.assertTrue(len(Person.get()) == 0)

    def test_person_model_repr(self):
        p = PersonModel()
        p.facebook_id = '123foo456'
        p.gender = 'male'
        p.name = "Foo Bar"
        p.username = "foo"
        self.assertRegex(str(p), "facebook_id='123foo456'")


class TestPersonAsync(TestPersonBase, tornado.testing.AsyncHTTPSTestCase):
    @patch('luiza_labs.business.person.AsyncHTTPClient')
    def test_save_from_facebook(self, mock_http_client):
        future = concurrent.futures.Future()
        response = HTTPResponse(HTTPRequest(''),
                                200,
                                buffer=BytesIO(b'{"id": "123foo456", "username": "foo", "first_name": "Foo", "last_name": "Bar", "gender": "male"}'))
        future.set_result(response)
        mock_http_client.return_value.fetch.return_value = future

        @gen.engine
        def f(callback):
            result = yield self.person.save_from_facebook('123foo456')
            self.assertTrue(result)
            callback()

        f(self.stop)
        p = self.person.get(1)[0]
        self.assertEqual('123foo456', p.facebook_id)
        self.wait()


if __name__ == '__main__':
    unittest.main()
