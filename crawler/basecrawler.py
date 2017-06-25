from bs4 import BeautifulSoup
import requests

from crawler.config import profile_urls


class BaseCrawler(object):
    """
    Crawler class, that can crawl different site for specific users
    """
    site = ''

    def __init__(self, hacker):
        self.username = hacker.username  # needed to show in error messages

        specific_username = hacker.get_site_account(self.site).specific_username
        self.profile_url = self.get_profile_url(specific_username)  # create profile url from username specific to site

    def get_profile_url(self, username):
        """Get url of hacker profile page from specific site."""
        return profile_urls[self.site].format(username)

    def get_page_content(self, site):
        """
        Gets page where score is on.
        :param site: site is the string with site abbreviation
        :return: BeautifulSoup object of the site where the score is on
        """
        with requests.Session() as crawl_session:
            # get the profile page where the scores are on
            request = crawl_session.get(self.profile_url)
            request.raise_for_status()

            request_content = request.content
            return BeautifulSoup(request_content, "html.parser")  # convert to BeautifulSoup response


class AccountDoesNotExist(Exception):
    def __init__(self, site, username):
        self.site = site
        self.username = username

    def __repr__(self):
        return '<Error: account {} from user {} does not exist>'.format(self.site, self.username)
