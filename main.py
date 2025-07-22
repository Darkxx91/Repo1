import http.server
import socketserver
import json
import cgi
from http.cookies import SimpleCookie

PORT = 8000
USERS_FILE = 'users.json'

def get_users():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        cookie = SimpleCookie(self.headers.get('Cookie'))
        if self.path == '/protected.html':
            if 'session' in cookie:
                username = cookie['session'].value
                users = get_users()
                if username in users:
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
            users = get_users()
            if username in users:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Username already exists')
            else:
                users[username] = password
                save_users(users)
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
            users = get_users()
            if username in users and users[username] == password:
                self.send_response(200)
                self.send_header('Set-Cookie', f'session={username}')
                self.end_headers()
                self.wfile.write(b'Login successful')
            else:
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b'Invalid credentials')

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
