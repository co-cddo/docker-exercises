#!/usr/bin/env python3

# We can run a webserver which serves static files from the current directory
# using 'python3 -m http.server PORT'. This script builds on the http module
# to print information about the request to the terminal. There's also some
# very basic error handling

import os
import optparse
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):

        print(f"Received GET request: {self.requestline}")
        print("\nHeaders:")
        for header in self.headers:
            print(f"{header}: {self.headers[header]}")
        client_address = self.client_address[0]
        print(f"\nClient Address: {client_address}")

        try:
            self.path = '/index.html' if self.path == '/' else self.path
            with open('.' + self.path, 'rb') as file:
                file_content = file.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(file_content)
        except FileNotFoundError:
            self.send_error(404, f'File not found: {self.path}')


def get_opts():
    parser = optparse.OptionParser()
    # Conventionally options would be lower-case but optparse reserves '-h'
    # for help
    parser.add_option("-H", "--host", dest="host", default="0.0.0.0")
    parser.add_option("-P", "--port", dest="port", type="int", default=8081)
    parser.add_option("-D", "--dir", dest="dir", default=os.getcwd())
    options, _ = parser.parse_args()
    return options


def run_server(host, port, root_dir):
    os.chdir(root_dir)
    web_server = HTTPServer((host, port), Handler)
    print('Server started http://{0}:{1}'.format(host, port))
    try:
        web_server.serve_forever()
    except Exception as e:  # This is better than `except:` but not much
        print(e)
    web_server.server_close()
    print('\nServer stopped.')


if __name__ == "__main__":
    options = get_opts()
    run_server(options.host, options.port, options.dir)
