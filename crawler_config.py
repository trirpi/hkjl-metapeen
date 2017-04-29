#!/usr/bin/env python

""" Configuration of crawler stuff """

# Floats stored that determine how many points you get for the site. (Some sites are easier then others)
callbacks = {
    'cs': 1.0,
    'hts': 30.0,
    'rm': 70.0,
    'otw': 9.0
}


# Urls that lead to user page of site
profile_urls = {
    'rm': 'https://root-me.org/{username}',
    'cs': 'https://certifiedsecure.nl/profile/{cs_id}',
    'otw': 'https://www.wechall.net/profile/{wechall_username}',
    'hts': 'https://www.hackthissite.org/user/view/{username}'
}