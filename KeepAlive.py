import http.server
import socketserver
import threading


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(b'Hello. I am alive!')

def run():
    with socketserver.TCPServer(('', 5050), Handler) as httpd:
        print('Server started')
        httpd.serve_forever()

def keep_alive():
    t = threading.Thread(target=run)
    t.start()