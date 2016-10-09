import tornado.web


class VersionHandler(tornado.web.RequestHandler):

    def get(self):
        data = {
            "version": "0.0.0",
        }
        self.write(data)
