import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from venmo_api import Venmo
import urlparse

class HandlerClass(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(s):
        s.send_response(200)
        s.send_header("Content-type","text/html")
        s.end_headers()
        try:
            ##TODO, compare state, better parser to    check params
            code = urlparse.urlparse(s.path)[4].split('=')[1]
            credentials = Venmo.exchange_token(code)
            Venmo.save_credentials(credentials)
            s.wfile.write('Your code has been saved in Alfred')
        except:
            s.wfile.write('Error with setting code')

ServerClass = BaseHTTPServer.HTTPServer
Protocol = "HTTP/1.0"

server_address = ('127.0.0.1', 1337)

HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, HandlerClass)

# Server is active for 20 seconds
httpd.timeout = 20
httpd.handle_request()
