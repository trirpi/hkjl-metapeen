#!/usr/bin/env python

""" Configuration of crawler stuff """

# Floats stored that determine how many points you get for the site. (Some sites are easier then others)
site_weights = {
    'cs': 1.0,
    'hts': 30.0,
    'rm': 70.0,
    'otw': 9.0,
    'ht': 20.0
}


# Urls that lead to user page of site
profile_urls = {
    'rm': 'https://root-me.org/{}',
    'cs': 'https://certifiedsecure.nl/profile/{}',
    'otw': 'https://www.wechall.net/profile/{}',
    'hts': 'https://www.hackthissite.org/user/view/{}',
    'ht': 'https://www.hackthis.co.uk/user/{}'
}


login_urls = {
    'ht': 'https://www.hackthis.co.uk/auth.php?login'
}