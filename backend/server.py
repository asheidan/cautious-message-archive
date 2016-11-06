import logging
import os.path

import tornado.httpserver
from tornado.options import options, parse_command_line
import tornado.web

from . import base_dir, run_as_application
from .routes import ROUTES

logger = logging.getLogger("tornado.application")

application = tornado.web.Application(ROUTES)


def setup_logging():
    global logger

    if run_as_application:
        log_file = os.path.realpath(os.path.join(
            base_dir, "..", "..", "logs", "python_archive.log"
        ))
    else:
        logging.basicConfig(level=logging.DEBUG)
        log_file = os.path.join(base_dir, "logs", "python_archive.log")

    logger = logging.getLogger("PythonArchive")
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=30000000, backupCount=10
    )
    handler.setLevel(logging.DEBUG)
    log_format = logging.Formatter("%(asctime)s - %(message)s")
    handler.setFormatter(log_format)
    logger.addHandler(handler)


def create_server():
    parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(port=options.http_port,
                       address=options.http_address)

    try:
        logger.info("Starting server listening on port %d", options.http_port)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        logger.warning("Caught KeyboardInterrupt, exiting....")
