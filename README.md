# Simple User Authentication

This is a simple user authentication system in Python.

## How to run

To run the web server, execute the following command:

```bash
python main.py
```

## How to use

### Registration

To register a new user, send a POST request to `http://localhost:8000/register` with the following parameters:

- `username`: the desired username
- `password`: the desired password

### Login

To login, send a POST request to `http://localhost:8000/login` with the following parameters:

- `username`: your username
- `password`: your password

If the login is successful, you will receive a session cookie.

### Protected Area

To access the protected area, navigate to `http://localhost:8000/protected.html`. You must be logged in to access this page.

### API

To get a JSON response from the API, navigate to `http://localhost:8000/api`.
