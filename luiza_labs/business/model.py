#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class PersonModel(Base):
    __tablename__ = 'person'
    facebook_id = Column(String(100), primary_key=True)
    name = Column(String(100))
    username = Column(String(50))
    gender = Column(String(6))

    def __repr__(self):
        return "<PersonModel(facebook_id='{}', name='{}', username='{}', gender='{}')>".format(
            self.facebook_id, self.name, self.username, self.gender
        )
