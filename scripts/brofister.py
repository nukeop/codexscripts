import argparse
import requests

from gooey import Gooey, GooeyParser
from tqdm import tqdm
from collections import OrderedDict

from login import login
from users import collect_post_ids

RATINGS = [("Brofist", 1), ("Agree", 2), ("Disagree", 3), ("Funny", 4), ("Salute", 5), ("Informative", 6),
           ("Friendly", 7), ("Fabulous", 9), ("Creative", 10), ("Old", 11), ("Bad Spelling", 12), ("Dumb", 13),
           ("Prestigious", 15), ("butthurt", 16), ("Racist", 17), ("Thanks!", 18), (",M (Parrot)", 19),
           ("Acknowledge this user's Agenda", 20), ("prosper", 21), ("Negative", 22), ("Doggy", 23),
           ("Excited!", 24), ("Shit", 25), ("Rage", 26), ("Citation Needed", 27), ("Undo rating", "del")]

# use an ordered dict to maintain order when converting to choices array
RATINGS = OrderedDict(RATINGS)


# Find all posts of a user and rate all of them.
@Gooey
def main():
    if __name__ == '__main__':
        parser = argparse.ArgumentParser(description='Brofist all posts of a user.')
        parser.add_argument('username', help="Your Codex username")
        parser.add_argument('password', help="Your Codex password")
        parser.add_argument('usertofist', help="User you want to rate")
        parser.add_argument('rating', choices=[k for k in RATINGS], help="Rating you want to give")

        args = parser.parse_args()

        session, data = login(args.username, args.password)

        ids = sorted(list(set(collect_post_ids(session, data, args.usertofist, "index.php?search/search", godeeper=True))))

        # Generate rate links via list comprehension
        rating_id = RATINGS[args.rating]
        ratelinks = ["http://www.rpgcodex.net/forums/index.php?posts/{0}/rate&rating={1}&_xfToken={2}".format(x, rating_id, data["_xfToken"]) for x in ids]

        # Set some data to enable responses in json
        data["users"] = None
        del data["users"]
        data["_xfResponseType"] = "json"
        data["_xfNoRedirect"] = 1

        # Engage fisting
        for link in tqdm(ratelinks):
            data["_xfRequestUri"] = link[23:]

            print "Fisting post in {}".format(link)
            session.post(link, data=data)

main()
