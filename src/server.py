"""
Server to handle redirect request
"""

# pylint: disable=relative-import, invalid-name, bare-except

import BaseHTTPServer
from venmo_api import Venmo
import urlparse

class HandlerClass(BaseHTTPServer.BaseHTTPRequestHandler):
    """Basic server class"""

    def do_GET(self):
        """Handle GET request to redirect URI"""

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        try:
            code = urlparse.urlparse(self.path)[4].split('=')[1]
            credentials = Venmo.exchange_token(code)
            Venmo.save_credentials(credentials)
            self.wfile.write('Your code has been saved in Alfred')
        except:
            self.wfile.write('Error with setting code')

ServerClass = BaseHTTPServer.HTTPServer
Protocol = "HTTP/1.0"

server_address = ('127.0.0.1', 1337)

HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, HandlerClass)

# Server is active for 20 seconds
httpd.timeout = 20
httpd.handle_request()
