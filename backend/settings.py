from tornado.options import define, options

define("http_port", type=int, default=8080,
       help="The port number to listen on.")

define("http_address", type=str, default="127.0.0.1",
       help="The ip-address to listen on.")
