#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from luiza_labs.business.model import *
import logging

log = logging.getLogger(__name__)


class Database():
    __instance = None

    def __init__(self):
        self.Base = Base
        self.engine = None
        self.session = None

    def connect(self, memory=False, host='localhost:3306', user='root', passwd='admin', db='luizalabs'):
        if memory:
            log.debug("Connect to SQLite in memory")
            self.engine = create_engine("sqlite:///:memory:")
        else:  # pragma: no cover
            log.debug("Connect to MySql [{}] with user {} in schema {}".format(host, user, db))
            self.engine = create_engine('mysql+pymysql://{}:{}@{}/{}'.format(user, passwd, host, db))
        self.session = sessionmaker(bind=self.engine)
        return True

    def setup(self):
        log.info("Create database structure")
        self.Base.metadata.create_all(self.engine)
        return True

    def uninstall(self):
        log.warning("Drop database structure")
        for tbl in reversed(Base.metadata.sorted_tables):
            self.engine.execute(tbl.delete())

    @staticmethod
    def get_instance():  # pragma: no cover
        if not Database.__instance:
            Database.__instance = Database()
        return Database.__instance
