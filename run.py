from app import app
from app.emails import start_scheduled_emails


if __name__ == '__main__':
    debug = True
    if not debug:
        start_scheduled_emails()
    app.run(debug=True)
