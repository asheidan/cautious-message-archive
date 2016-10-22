from tornado.options import define, options

define("http_port", type=int, default=8080,
       help="The port number to listen on.")
