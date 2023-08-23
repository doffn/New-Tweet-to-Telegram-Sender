import http.server
import socketserver
import threading
import random

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Hello. I am alive!')

def run():
    port = random.randint(8000, 9000)  # Generate a random port number between 8000 and 9000
    with socketserver.TCPServer(('', port), Handler) as httpd:
        print(f'Server started on port {port}')
        httpd.serve_forever()

def keep_alive():
    t = threading.Thread(target=run)
    t.start()