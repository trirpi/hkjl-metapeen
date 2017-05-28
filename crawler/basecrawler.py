from bs4 import BeautifulSoup
import requests

from crawler.config import profile_urls, login_urls
import credentials


class BaseCrawler(object):
    """
    Crawler class, that can crawl different site for specific users
    """
    site = ''

    def __init__(self, hacker):
        self.username = hacker.username  # needed to show in error messages
        self.profile_url = self.get_profile_url(hacker.get_site_account(self.site).specific_username)  # create profile url from username specific to site

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
            if site in login_urls:  # you need to login to access points
                crawl_session.post(login_urls[site], credentials.callbacks[site])

            # get the profile page where the scores are on
            request = crawl_session.get(self.profile_url).content
            return BeautifulSoup(request, "html.parser")  # convert to BeautifulSoup response
