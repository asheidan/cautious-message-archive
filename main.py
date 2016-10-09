import logging
import logging.handlers
import os
import sys

import webview

from backend.server import create_server

run_as_application = getattr(sys, "frozen", False)
logger = None

if run_as_application:
    resource_dir = os.path.realpath(os.path.dirname(__file__))
    base_dir = os.path.realpath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
    log_file = os.path.realpath(os.path.join(
        base_dir, "..", "..", "logs", "python_archive.log"
    ))
else:
    resource_dir = os.path.realpath(os.path.join(
        os.path.dirname(__file__), "frontend", "dist"
    ))
    base_dir = os.path.realpath(os.path.dirname(__file__))
    log_file = os.path.join(base_dir, "logs", "python_archive.log")


def setup_logging():
    global logger
    logger = logging.getLogger("PythonArchive")
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=30000000, backupCount=10
    )
    handler.setLevel(logging.DEBUG)
    log_format = logging.Formatter("%(asctime)s - %(message)s")
    handler.setFormatter(log_format)
    logger.addHandler(handler)

setup_logging()
logger.debug("Base directory: %s", base_dir)

index_path = os.path.join(resource_dir, "html", "index.html")
index_url = "file://%s" % index_path
logger.debug("Index URL: %s", index_url)

webview.create_window("MessageArchive", index_url,
                      width=800, height=600,
                      resizable=True, fullscreen=False)
