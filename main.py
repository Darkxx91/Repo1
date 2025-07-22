import http.server
import socketserver
import json
import cgi
from http.cookies import SimpleCookie
import random
import database

PORT = 8000
QUOTES_FILE = 'quotes.json'

def get_quotes():
    with open(QUOTES_FILE, 'r') as f:
        return json.load(f)

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        cookie = SimpleCookie(self.headers.get('Cookie'))
        if self.path == '/protected.html':
            if 'session' in cookie:
                username = cookie['session'].value
                user = database.get_user(username)
                if user:
                    super().do_GET()
                else:
                    self.send_response(401)
                    self.end_headers()
                    self.wfile.write(b'Unauthorized')
            else:
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b'Unauthorized')
        elif self.path == '/api':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'message': 'Hello, World!'}).encode())
        elif self.path == '/api/quote':
            if 'session' in cookie:
                username = cookie['session'].value
                user = database.get_user(username)
                if user and user['subscribed']:
                    quotes = get_quotes()['quotes']
                    quote = random.choice(quotes)
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'quote': quote}).encode())
                else:
                    self.send_response(401)
                    self.end_headers()
                    self.wfile.write(b'Unauthorized')
            else:
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b'Unauthorized')
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/register':
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            username = form.getvalue('username')
            password = form.getvalue('password')
            user = database.get_user(username)
            if user:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Username already exists')
            else:
                database.create_user(username, password)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'Registration successful')
        elif self.path == '/login':
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            username = form.getvalue('username')
            password = form.getvalue('password')
            user = database.get_user(username)
            if user and user['password'] == password:
                self.send_response(200)
                self.send_header('Set-Cookie', f'session={username}')
                self.end_headers()
                self.wfile.write(b'Login successful')
            else:
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b'Invalid credentials')
        elif self.path == '/subscribe':
            cookie = SimpleCookie(self.headers.get('Cookie'))
            if 'session' in cookie:
                username = cookie['session'].value
                user = database.get_user(username)
                if user:
                    database.subscribe_user(username)
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'Subscription successful')
                else:
                    self.send_response(401)
                    self.end_headers()
                    self.wfile.write(b'Unauthorized')
            else:
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b'Unauthorized')

if __name__ == '__main__':
    database.init_db()
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()
