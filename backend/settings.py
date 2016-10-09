from tornado.options import define

define("http_port", type=int, default=8080,
       help="The port number to listen on.")
