from flask import render_template
from flask_mail import Message
from app import mail, db, app
from app.models import User, Assignment, UserAssignments
from threading import Thread
from config import MAIL_SERVER, ADMINS
import datetime
from threading import Timer


def send_async_email(app, msg):
    """
    Target function run in thread to send email. Used by send_email.
    """
    with app.app_context():
        mail.send(msg)


def send_email(subject, recipients, text_body, html_body, sender='no_reply@' + MAIL_SERVER):
    """
    Sends an email to a recipient from the configured mail server.
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    # mail sending is slow, do asynchronously
    th = Thread(target=send_async_email, args=[app, msg])
    th.start()


def send_email_admin_asgndue(assignment):
    """
    Send email to admin about assignment whose due date has passed.

    Email contains assignment title, due date, people who completed it,
    people who tried and failed, and people who didn't try it at all.

    Args:
        assignment (Assignment): Assignment now due.
    """
    send_email(
        "Assignment due date passed",
        [ADMINS[0]],
        render_template('emails/txt/admin_asgndue_email.txt'),
        render_template('emails/html/admin_asgndue_email.html')
    )


def send_email_admin_late_soln(user_soln):
    """
    Send email to admin for when user has completed an assignment late.

    Email contains user name, email, which assignment they completed, when
    it was due and when they completed it.

    Args:
        user_soln (UserAssignments): Solution user has posed.
    """
    send_email(
        "User solved assignment late",
        [ADMINS[0]],
        render_template('emails/txt/admin_late_soln_email.txt'),
        render_template('emails/html/admin_late_soln_email.html')
    )


def send_email_user_asgn_soon(assignment):
    """
    Send email to all users when an assignment is due in 24 hours that has not been completed.

    Args:
        assignment (Assignment): Assignment to be due in 24 hours.
    """
    users = [user for user in User.query.all() if not user.has_solved(assignment)]
    send_email(
        "Assignment due in 24 hours",
        users,
        render_template('emails/txt/user_asgn_soon_email.txt'),
        render_template('emails/html/user_asgn_soon_email.html')
    )


def send_email_user_asgn_due(assignment):
    """
    Send email to all users who have not completed an assignment whose due date has passed.

    Args:
        assignment (Assignment): Assignment now due.
    """
    users = [user for user in User.query.all() if not user.has_solved(assignment)]
    send_email(
        "Assignment not completed",
        users,
        render_template('emails/txt/user_asgn_due_email.txt'),
        render_template('emails/html/user_asgn_due_email.html')
    )


def send_email_users_new_asgn(assignment):
    """
    Send email to all users when a new assignment has been issued.

    Args:
        assignment (Assignment): New assignment to send note of.
    """
    send_email(
        "New assignment available!",
        User.query.all(),
        render_template('emails/txt/user_new_asgn_email.txt'),
        render_template('emails/html/user_new_asgn_email.html')
    )


def send_scheduled_emails():
    """
    Check criteria for sending each email and send it if need be.
    Scheduled to run every ten minutes (600 seconds).
    Does not send 'users_new_asgn' or 'admin_late_soln'; these are sent when they happen.
    """
    for assignment in Assignment.query.all():
        tdelta = datetime.datetime.now().date() - assignment.date_due
        if 0 < tdelta.total_seconds() - (24 * 3600) <= 600:     # <= 10 minutes until 24 hours to asgn's due date
            send_email_user_asgn_soon(assignment)
        elif -600 < tdelta.total_seconds() <= 0:    # assignment due date passed < 10 mins ago
            send_email_admin_asgndue(assignment)
            send_email_user_asgn_due(assignment)
    # do again in 10 minutes, in another thread
    timer = Timer(600, send_scheduled_emails)
    timer.start()


def start_scheduled_emails():
    """
    Start sending scheduled emails as they are needed.
    """
    # no initialization needed at the moment, keep this function in case
    timer = Timer(600, send_scheduled_emails)
    timer.start()
