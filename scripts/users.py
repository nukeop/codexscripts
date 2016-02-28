import argparse
import re
import requests

from constants import POST_URL_REGEX, SEARCHPAGES_REGEX, FIND_OLDER_REGEX, PAGENAV_CLASS, base_url

def collect_post_ids(session, data, username, searchurl, visited=[], godeeper=False, fetcholder=False):
    """Builds a list of a given user's posts.
    
    Depending on the parameters, this function will either:
    - return the ids of posts found on a page designated by searchurl argument
    - return the above and also check for further pages of search results and add the ids from those pages, calling this function recursively for each page
    - return the above and call this function recursively on the page returned by clicking 'show older posts'

    It needs an active session, data dict with _xfToken entry (both provided by the login function from login module), username whose posts are to be retrieved, and a searchurl (added to base path, in general it will be 'index.php?search/search').

    'visited' argument is only used in recursive calls to keep track of already visited pages.

    'godeeper' decides if the algorithm should visit further pages (there are 20 posts per page so a maximum of 5 pages)

    'fetcholder' decides if the search should continue after reaching the last page of search results and there are older posts (codex search function returns only the first 100 posts matching the search terms)
    """
    
    url = base_url + searchurl
    print "Visiting {0}".format(url)

    #Set the user whose posts are to be retrieved and visit the url
    data["users"] = username
    response = session.post(url, data=data)
    html = response.text.encode('utf-8')
    
    postnums = []
    searchpages = []
    findolder = ""

    #Check if there are any posts found
    if not "No results" in html:

        #Build a list of post ids, optionally visiting further pages
        beg = html.find('<div class="PageNav"')
        end = html.rfind('<div class="PageNav"')

        for line in html[beg:end].split():
            m = re.search(POST_URL_REGEX, line)
            if m:
                postnums.append(m.group("postnum"))

            if godeeper:
                m = re.search(SEARCHPAGES_REGEX, line)
                if m:
                    searchpages.append(m.group("link"))

            if fetcholder:
                m = re.search(FIND_OLDER_REGEX, line)
                if m:
                    findolder = m.group("link")
                    
        #Remove duplicates from further pages to search
        searchpages = sorted(list(set([x.replace("&amp;", "&") for x in searchpages])))

        #Call the function recursively on further pages
        for i in range(len(searchpages)):

            if(searchpages[i] not in visited):
                visited.append(searchpages[i])
            
                if i == 0:
                    postnums.extend(collect_post_ids(session, data, username, searchpages[i], visited=visited, godeeper=True))
                elif i == len(searchpages)-1:
                    postnums.extend(collect_post_ids(session, data, username, searchpages[i], visited=visited, fetcholder=True))
                else:
                    postnums.extend(collect_post_ids(session, data, username, searchpages[i], visited=visited))

        if findolder is not "":
            postnums.extend(collect_post_ids(session, data, username, findolder.replace("&amp;", "&"), visited=visited, godeeper=True))            

        return postnums
    else:
        print "No results found"
        return []


#If running as a script, log in with provided credentials, search for a particular user's posts, and print a list of urls of those posts
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find all posts of a user.')
    parser.add_argument('username')
    parser.add_argument('password')
    parser.add_argument('usertostalk')

    args = parser.parse_args()

    from login import login

    session, data = login(args.username, args.password)
    
    l = sorted(list(set(collect_post_ids(session, data, args.usertostalk, "index.php?search/search", godeeper=True))))

    print "Total posts: {}".format(len(l))
    for id in l:
        print "http://www.rpgcodex.net/forums/index.php?posts/{}/".format(id)
