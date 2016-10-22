import logging
import logging.handlers
import os
import sys
import threading

import webview

from backend import base_dir, resource_dir
from backend.server import create_server
from backend.server import setup_logging

logger = logging.getLogger("PythonArchive")

setup_logging()
logger.debug("Base directory: %s", base_dir)

index_path = os.path.join(resource_dir, "html", "index.html")
index_url = "file://%s" % index_path
logger.debug("Index URL: %s", index_url)

thread = threading.Thread(target=create_server)
thread.daemon = True
thread.start()

webview.create_window("MessageArchive", index_url,
                      width=800, height=600,
                      resizable=True, fullscreen=False)
