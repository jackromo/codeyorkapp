"""
File: asgntest_client.py

Client program for admin managing assignment tests off-server.
"""

import sys
import json
import urllib2


site_url = 'http://parseltongue.net'

secret_key = 'i-totally-thought-of-a-good-key-m8-lmao-get-rekked-hax0rs'


# Edit these dicts to send different requests

added_test_json = {
    'key': secret_key,
    'asgn_id': 1,
    'test_inp': 'input',
    'test_out': 'out'
}

del_test_json = {
    'key': secret_key,
    'test_id': 2
}

get_all_test_json = {
    'key': secret_key
}


def make_request(path, data):
    req = urllib2.Request(site_url + path)
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(data))
    print response.read()


def handle_bad_args():
    print "Usage: python asgntest_client.py --[add|del|getall] args"


def main(args):
    if len(args) != 2:
        handle_bad_args()
    elif args[1] == '--add':
        make_request('/addtest', added_test_json)
    elif args[1] == '--del':
        make_request('/deltest', del_test_json)
    elif args[1] == '--getall':
        make_request('/getalltests', get_all_test_json)
    else:
        handle_bad_args()


if __name__ == '__main__':
    main(sys.argv)
