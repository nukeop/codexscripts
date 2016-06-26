import argparse
import requests

from gooey import Gooey, GooeyParser
from tqdm import tqdm

from login import login
from users import collect_post_ids

@Gooey
def main():
#Find all posts of a user and brofist all of them.
    if __name__ == '__main__':
        parser = argparse.ArgumentParser(description='Brofist all posts of a user.')
        parser.add_argument('username', help="Your Codex username")
        parser.add_argument('password', help="Your Codex password")
        parser.add_argument('usertofist', help="User you want to fist")

        args = parser.parse_args()

        session, data = login(args.username, args.password)

        ids = sorted(list(set(collect_post_ids(session, data, args.usertofist, "index.php?search/search", godeeper=True))))

        #Generate brofist links via list comprehension
        brofistlinks = ["http://www.rpgcodex.net/forums/index.php?posts/{0}/like".format(x) for x in ids]

        #Set some data to enable responses in json
        data["users"] = None
        del data["users"]
        data["_xfResponseType"] = "json"
        data["_xfNoRedirect"] = 1

        #Engage fisting
        for link in tqdm(brofistlinks):
            data["_xfRequestUri"] = link[23:]

            print "Fisting post in {}".format(link)
            response = session.post(link, data=data)

            #Check if we brofisted or brolapsed - if we brolapsed, brofist again
            json = response.json()
            if json["term"] == "Brofist":
                response = session.post(link, data=data)

main()
