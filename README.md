# Car Project AWS Deployment

This project is a Flask app with MySQL storage for user accounts and car inquiries.

## Environment Variables

Set these values in your AWS environment instead of hardcoding them in the app:

- `FLASK_SECRET_KEY`
- `FLASK_DEBUG`
- `PORT`
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`

You can use [.env.example](/Users/younus/Downloads/carproject/.env.example) as the template for your values.

## Local Run

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Export environment variables.
4. Start the app:

```bash
python app.py
```

## Production Run

Run the app with Gunicorn:

```bash
gunicorn wsgi:application
```

## AWS EC2 Outline

1. Launch an EC2 instance.
2. Install Python 3, `pip`, and Nginx.
3. Copy this project onto the server.
4. Create a virtual environment and install `requirements.txt`.
5. Set environment variables for Flask and your AWS RDS MySQL database.
6. Start Gunicorn with `gunicorn wsgi:application --bind 0.0.0.0:5000`.
7. Put Nginx in front of Gunicorn as the public web server.

## AWS Elastic Beanstalk Outline

1. Create a Python Elastic Beanstalk environment.
2. Upload this project with `requirements.txt` and `Procfile`.
3. Add the environment variables in the Elastic Beanstalk console.
4. Point the DB variables to your RDS MySQL instance.
5. Deploy.

## Database Notes

The app creates the `car_inquiries` table automatically at startup if it does not already exist.

Make sure your `users` table includes an `id` primary key, because inquiries link back to `users(id)`.
