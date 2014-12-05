#!/usr/bin/env python
# -*- coding: utf-8 -*-

from luiza_labs.integrations.database import Database
from luiza_labs.business.model import PersonModel
from tornado.httpclient import AsyncHTTPClient
from tornado import gen
import json
import logging

log = logging.getLogger(__name__)


class Person():
    @staticmethod
    @gen.coroutine
    def save_from_facebook(facebook_id):
        log.debug("get facebook data of [{}]".format(facebook_id))
        url = 'https://graph.facebook.com/%s' % facebook_id
        http_return = yield AsyncHTTPClient().fetch(url)

        log.debug("manipulate return of facebook request")
        p = Person.graph_to_person_model(http_return.body.decode())

        log.info("save user [{}]".format(p.name))
        session = Database.get_instance().session()
        session.add(p)
        session.commit()
        return True

    @staticmethod
    def graph_to_person_model(data):
        user_data = json.loads(data)
        p = PersonModel()
        p.facebook_id = user_data['id']
        p.name = "{} {}".format(user_data['first_name'], user_data['last_name'])
        p.username = user_data['username']
        p.gender = user_data['gender']
        return p

    @staticmethod
    def get(limit=0):
        session = Database.get_instance().session()
        log.debug('list all user' if limit == 0 else 'get {} user(s)'.format(limit))
        q = session.query(PersonModel)
        if limit > 0:
            q = q.limit(limit)
        return q.all()

    @staticmethod
    def delete(facebook_id):
        log.warning("Delete user [{}]".format(facebook_id))
        session = Database.get_instance().session()
        session.query(PersonModel).filter_by(facebook_id=facebook_id).delete()
        session.commit()
        return True
