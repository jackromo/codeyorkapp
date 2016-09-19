"""
File: asgn_client.py

Client program for admin managing assignments off-server.
"""

import sys
import json
import urllib2
import datetime


site_url = 'http://parseltongue.net'

secret_key = 'i-totally-thought-of-a-good-key-m8-lmao-get-rekked-hax0rs'


# Edit these dicts to send different requests

added_asgn_json = {
    'key': secret_key,
    'title': 'New assignment',
    'desc': 'This is a new assignment.',
    'visible': True,
    'date_due': datetime.date.toordinal(datetime.date.today())
}

del_asgn_json = {
    'key': secret_key,
    'asgn_id': 1
}

get_all_asgn_json = {
    'key': secret_key
}

edit_asgn_json = {
    'key': secret_key,
    'asgn_id': 1,
    'title': 'New Title',
    'desc': 'This is the new description.',
    'visible': True,
    'date_due': datetime.date.toordinal(datetime.date.today())
}


def make_request(path, data):
    req = urllib2.Request(site_url + path)
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(data))
    print response.read()


def handle_bad_args():
    print "Usage: python asgn_client.py --[add|del|getall|edit] args"


def main(args):
    if len(args) != 2:
        handle_bad_args()
    elif args[1] == '--add':
        make_request('/addassignment', added_asgn_json)
    elif args[1] == '--del':
        make_request('/delassignment', del_asgn_json)
    elif args[1] == '--getall':
        make_request('/getassignments', get_all_asgn_json)
    elif args[1] == '--edit':
        make_request('/editassignment', edit_asgn_json)
    else:
        handle_bad_args()


if __name__ == '__main__':
    main(sys.argv)
