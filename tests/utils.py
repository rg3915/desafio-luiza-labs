#!/usr/bin/env python
# -*- coding: utf-8 -*-

from luiza_labs.integrations.database import Database
from luiza_labs.business.model import PersonModel


def make_mock_database_connection():
    database = Database()
    database.connect(memory=True)
    database.setup()
    Database._Database__instance = database
    return database


def clear_mock_database(database):
    database.uninstall()
    Database._Database__instance = None


def data_for_testing(session):
    p1 = PersonModel()
    p1.facebook_id = '123foo456'
    p1.name = "Foo Bar"
    p1.username = "foo"
    p1.gender = "female"

    p2 = PersonModel()
    p2.facebook_id = "bar_111222"
    p2.name = "Bar Foo"
    p2.username = "Bar"
    p2.gender = "male"

    session.add(p1)
    session.add(p2)
    session.commit()
