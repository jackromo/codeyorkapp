"""
File: asgn_mod.py

Helper script for admin managing assignments on-server.
"""

import sys
import datetime
from app import db, models


class BadArgumentsException(Exception):

    def __init__(self, message):
        super(Exception, self).__init__("Usage: python asgn_mod.py " + message)


def handle_command(args, handler, arg_count_ls, error_msg):
    if len(args) not in arg_count_ls:
        raise BadArgumentsException(error_msg)
    return handler(args)


def handle_add(args):
    assignment = models.Assignment(
        title=args[2],
        desc=args[3],
        visible=bool(args[4]),
        date_due=datetime.date(int(args[5]), int(args[6]), int(args[7]))
    )
    db.session.add(assignment)
    db.session.commit()
    if assignment.visible:
        emails.send_email_users_new_asgn(assignment)
    return "Added assignment " + str(assignment) + " successfully."


def handle_del(args):
    asgn = models.Assignment.query.filter(models.Assignment.id == int(args[2])).first()
    db.session.delete(asgn)
    return_str = "Assignment " + str(asgn) + " deleted successfully."
    db.session.commit()
    return return_str


def handle_edit(args):
    visible_before = asgn.visible
    new_attrs = args[4:][::-1]
    config_arg = args[3]
    while len(config_arg) > 0:
        if config_arg[0] == 'n':
            asgn.title = new_attrs.pop()
        elif config_arg[0] == 'd':
            asgn.desc = new_attrs.pop()
        elif config_arg[0] == 'v':
            asgn.visible = bool(new_attrs.pop())
        elif config_arg[0] == 't':
            year = int(new_attrs.pop())
            month = int(new_attrs.pop())
            day = int(new_attrs.pop())
            asgn.date_due = datetime.date(year, month, day)
        else:
            raise BadArgumentsException("--edit asgn_id [n][d][v][t] args")
        config_arg = config_arg[1:]
    db.session.commit()
    if asgn.visible and not visible_before:
        send_email_users_new_asgn(asgn)
    return "Assignment edited successfully."


def handle_getall(args):
    asgn_ls = []
    for asgn in models.Assignment.query.all():
        asgn_ls.append(
            "<id=%s title=\"%s\" desc=\"%s\" visible=%s datedue=%s>" % (
                str(asgn.id),
                asgn.title,
                asgn.desc,
                str(asgn.visible),
                str(asgn.date_due)
            )
        )
    return "\n".join(asgn_ls)


def main(args):
    try:
        if len(args) < 2:
            raise BadArgumentsException("--[add|del|getall|edit] args")
        elif args[1] == '--add':
            print handle_command(args, handle_add, [8], "--add \"title\" \"desc\" int(visible) yeardue monthdue daydue")
        elif args[1] == '--del':
            print handle_command(args, handle_add, [3], "--del asgn_id")
        elif args[1] == '--getall':
            print handle_command(args, handle_add, [2], "--getall")
        elif args[1] == '--edit':
            print handle_command(args, handle_edit, range(4, 11), "--edit asgn_id [n][d][v][t] \"title\" \"desc\" int(visible) year month day")
        else:
            raise BadArgumentsException("--[add|del|getall|edit] args")
    except BadArgumentsException as e:
        print e.message


if __name__ == '__main__':
    main(sys.argv)

