from app import app
from app.emails import start_scheduled_emails
import sys


if __name__ == '__main__':
    if len(sys.argv) > 1:
        debug = (sys.argv[1] == '--debug')
    else:
        debug = False
    if not debug:
        start_scheduled_emails()
    app.run(debug=debug)
