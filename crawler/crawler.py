from bs4 import BeautifulSoup
import requests

from crawler_config import profile_urls, login_urls
import credentials
from crawler import crawl_functions
from peen import db


class Crawler(object):
    """
    Crawler class, that can crawl different site for specific users
    """
    def __init__(self):
        pass

    @staticmethod
    def get_profile_url(site, username):
        """Get url of hacker profile page from specific site"""
        return profile_urls[site].format(username)

    def get_score(self, site, username):
        """
        Scrapes score of sites
        :param site: accepts string with site abbreviation
        :param username: the username of user
        :return: exact score that the user has on the site
        :rtype: int
        """
        with requests.Session() as session:
            if site in login_urls:  # you need to login to access points
                g = session.post(login_urls[site], credentials.callbacks[site])

            # get the profile page where the scores are on
            url = self.get_profile_url(site, username)
            request = session.get(url).content

        bs_response = BeautifulSoup(request, "html.parser")  # convert to BeautifulSoup response
        score = crawl_functions.callbacks[site](bs_response)  # get score
        return score


def update_score(hacker, site=None):
    """
    Update scores of a user.
    :param hacker: person whose score should be updated
    :type hacker: Hacker class instance
    :param site: site that needs to be updated (if none it updates all scores)
    :return: None
    
    :Example:
    
    >>> from peen.orm.models import Hacker
    >>> hacker = Hacker.query.filter_by(username='henk').first()
    >>> update_score(hacker, site='rm')
    """
    crawler = Crawler()
    scores = hacker.scores  # list with username/id and current score
    username = hacker.username
    if site is None:  # update scores of all sites the user has
        for site_key in scores:
            score = crawler.get_score(site_key, username)  # get score
            hacker.update_score(site_key, score)  # set new values
    else:  # update the specific site
        score = crawler.get_score(site, username)  # get score
        hacker.update_score(site, score)  # set new values

    db.session.commit()  # and put them in the db

if __name__ == '__main__':
    crawl = Crawler()
    print(crawl.get_score('ht', 'trirpi'))
