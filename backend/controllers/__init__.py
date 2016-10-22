import tornado.web

from .. import __version__


class VersionHandler(tornado.web.RequestHandler):

    def get(self):
        data = {
            "version": __version__,
        }
        self.write(data)
