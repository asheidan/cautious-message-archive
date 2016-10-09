import logging

import tornado.httpserver
from tornado.options import options
import tornado.web

from .routes import ROUTES

logger = logging.getLogger("tornado.application")

application = tornado.web.Application(ROUTES)


def create_server():
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(port=options.http_port)

    try:
        logger.info("Starting server listening on port %d", options.http_port)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        logger.warning("Caught KeyboardInterrupt, exiting....")

    return http_server
