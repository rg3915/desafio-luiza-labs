#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.web import RequestHandler
from tornado import gen
from tornado.httpclient import HTTPError
from luiza_labs.business.person import Person
from json import dumps


class PersonHandler(RequestHandler):
    def response_http(self, body=None, status=200):
        self.set_status(status)
        if body:
            self.write(dumps(body))
        self.finish()

    @gen.coroutine
    def post(self):
        facebook_id = self.get_body_argument('facebookId', None)
        try:
            if facebook_id:
                yield Person.save_from_facebook(facebook_id)
                self.response_http(status=201)
            else:
                raise Exception("facebookId required")
        except HTTPError as err:
            self.response_http(body=err.response.body.decode(),
                               status=err.code)
        except Exception as err:
            self.response_http(body={"error": str(err)},
                               status=500)

    def get(self):
        limit = self.get_argument('limit', 0)
        result = [{"facebook_id": p.facebook_id,
                   "name": p.name,
                   "username": p.username,
                   "gender": p.gender} for p in Person.get(int(limit))]
        self.response_http(body=result)

    def delete(self, facebook_id):
        Person.delete(facebook_id)
        self.response_http(status=204)
