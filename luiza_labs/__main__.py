#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.getcwd())

import tornado.ioloop
import tornado.web
from tornado.options import define, options, parse_command_line
import luiza_labs.handlers.api as api
from luiza_labs.integrations.database import Database
import logging


def main():
    define("memory", default="False", help="Using database in memory")
    define("mysql_host", default='localhost:3306', help="MySql hostname and port")
    define("mysql_user", default='root', help="MySql username")
    define("mysql_passwd", default='admin', help="MySql password")
    define("mysql_db", default="luizalabs", help="Default database working in MySql")
    define("http_port", default='8888', help="Port of HTTP server")
    parse_command_line()

    log = logging.getLogger(__name__)
    try:
        log.info("Connect to database")
        db = Database.get_instance()
        db.connect(memory=options.memory == "True",
                   host=options.mysql_host,
                   user=options.mysql_user,
                   passwd=options.mysql_passwd,
                   db=options.mysql_db)
        db.setup()

        app = tornado.web.Application([
            (r"/person/?", api.PersonHandler),
            (r"/person/([^/]+)/?", api.PersonHandler)
        ])
        app.listen(int(options.http_port))
        log.info("Start Server")
        tornado.ioloop.IOLoop.instance().start()
    except Exception as err:
        log.exception(err)

if __name__ == "__main__":
    main()
