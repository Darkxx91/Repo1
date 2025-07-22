# Daily Quote Subscription Service

This is a simple subscription-based service that provides access to a "daily quote" API.

## How to set up

1. Clone the repository.
2. Install the dependencies: `pip install -r requirements.txt`
3. Initialize the database: `python database.py`

## How to run locally

To run the web server locally, execute the following command:

```bash
python main.py
```

## How to deploy to Heroku

1. Create a Heroku account.
2. Install the Heroku CLI.
3. Login to Heroku: `heroku login`
4. Create a new Heroku app: `heroku create`
5. Push the code to Heroku: `git push heroku main`
6. Open the app in your browser: `heroku open`

## How to use

### Registration

To register a new user, send a POST request to `/register` with the following parameters:

- `username`: the desired username
- `password`: the desired password

### Login

To login, send a POST request to `/login` with the following parameters:

- `username`: your username
- `password`: your password

If the login is successful, you will receive a session cookie.

### Pricing

To view the pricing page, navigate to `/pricing.html`.

### Subscription

To subscribe to the service, click the "Subscribe" button on the pricing page. You must be logged in to subscribe.

### Daily Quote API

To get a random quote from the API, navigate to `/api/quote`. You must be subscribed to access this API.

### Protected Area

To access the protected area, navigate to `/protected.html`. You must be logged in to access this page.

### API

To get a JSON response from the API, navigate to `/api`.

## How to run tests

To run the tests, execute the following command:

```bash
python test_main.py
```
