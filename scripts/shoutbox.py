import argparse
import re
import requests
import time

from lxml import html, etree

from constants import base_url
from login import login

START_TAGS_REGEX = re.compile("<.*?>(.*)")
END_TAGS_REGEX = re.compile("(.*)<\/.*?>")

def send_message(msg, color, data, session):
    url = base_url + "index.php?taigachat/post.json"
    data['message'] = msg
    data['_xfRequestUri'] = "/forums/index.php"
    data['room'] = '1'
    data['color'] = color
    response = session.post(url, data=data)
    print response

def receive_messages(data, session):
    url = base_url + "data/taigachat/messagesmini.html?"
    data['_xfRequestUri'] = "/forums/index.php"
    data['_xfNoRedirect'] = '1'
    data['_xfResponseType'] = "json"
    data['_'] = "1469138139650"
    response = session.get(url, params=data)
    try:
        return response.json()
    except ValueError:
        return None

def clean_tags(msg):
    while START_TAGS_REGEX.match(msg):
        msg = START_TAGS_REGEX.split(msg)[1]

    while END_TAGS_REGEX.match(msg):
        msg = END_TAGS_REGEX.split(msg)[1]

    return msg

def get_num_users(msgs):
    return msgs['numInChat']

def get_motd(msgs):
    return msgs['motd']

def parse_messages(msgs):
    """Parses messages, returns tuples (author, message)
    """
    tuples = []
    for message in [x['html'] for x in msgs['messages']]:
            tree = html.fromstring(message)
            author = tree.xpath('//li/span/a/text()')[0]
            shout = tree.xpath('//li/span/div')

            if shout[0].text is not None:
                shout = shout[0].text
            else:
                try:
                    shout = etree.tostring(shout[0].xpath("span")[0])
                except IndexError:
                    shout = etree.tostring(shout[0])

            shout = shout.encode('utf-8')
            shout = clean_tags(shout)
            tuples.append((author, shout))
    return tuples

def main():
    parser = argparse.ArgumentParser(description='Interact with the shoutbox.')
    parser.add_argument('username', help="Your Codex username")
    parser.add_argument('password', help="Your Codex password")

    args = parser.parse_args()

    session, data = login(args.username, args.password)

    allmsg = []

    msgs = receive_messages(data, session)

    print "Users in chat: {}".format(get_num_users(msgs))
    print "MOTD: {}".format(get_motd(msgs))

    while True:
        msgs = receive_messages(data, session)

        tuples = parse_messages(msgs)
        for t in tuples:
            entry = "{}: {}".format(
               t[0],
               t[1]
            )

            if entry not in allmsg:
               allmsg.append(entry)
               print entry

        time.sleep(1)

if __name__=='__main__':
    main()
