import argparse
import re
import requests

from constants import base_url, XFTOKEN_REGEX

def login(user, passw):
    """Tries to log in with a username and a password.

    Returns a new active session and request data.
    """
    #Create vars to return
    s, data = None, None
    
    #Begin a new session and connect to the forum
    url = base_url + "index.php"
    s = requests.Session()
    s.post(url)

    #Try logging in
    url = base_url + "index.php?login/login"
    data = {"_xfToken":"", "login":user, "password":passw, "register":0, "cookie_check":1, "redirect":"/forums/index.php"}
    response = s.post(url, data=data)

    #Look for _xfToken in the received html
    m = re.search(XFTOKEN_REGEX, response.text.encode('utf-8'))
    if m:
        data = {}
        data["_xfToken"] = m.group("token")

        print "Logged in successfully as {}.".format(user)
    else:
        print "Logging in unsuccessful. Check your username and/or password."
    
    return s, data
    

#If running as a script, get username and password from arguments and try to log in, then print the cookies and _xfToken
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Log into Codex.')
    parser.add_argument('username')
    parser.add_argument('password')

    args = parser.parse_args()
    
    session, data = login(args.username, args.password)

    print "\nCookies:\n"
    for cookie in session.cookies:
        print cookie

    print "\nData:\n"
    print data
    
