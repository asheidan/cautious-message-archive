from tornado.web import URLSpec

from .controllers import VersionHandler


ROUTES = [
    URLSpec(r"/version", VersionHandler, name="version"),
]
