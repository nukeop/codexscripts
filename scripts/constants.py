import re

POST_URL_REGEX = re.compile('href="index\.php\?posts/(?P<postnum>[0-9]{2,7})')

SEARCHPAGES_REGEX = re.compile('href="(?P<link>index\.php\?search/(?P<searchid>[0-9]{3,9})/&amp;page=[0-9])')

FIND_OLDER_REGEX = re.compile('href="(?P<link>index\.php\?search/member&amp;user_id=[0-9]{2,6}&amp;before=[0-9]{8,11}")')

PAGENAV_CLASS = '<div class="PageNav"'

XFTOKEN_REGEX = re.compile('name="_xfToken" value="(?P<token>[0-9a-f,]+)"')

base_url = "http://www.rpgcodex.net/forums/"
