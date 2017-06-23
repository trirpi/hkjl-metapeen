import requests
from bs4 import BeautifulSoup

from crawler.basecrawler import BaseCrawler, AccountDoesNotExist
from crawler.config import login_urls
import credentials


class HTCrawler(BaseCrawler):
    """Crawler for hackthis.co.uk."""
    site = 'ht'

    def get_page_content(self, site):
        """
        Gets page where score is on.
        :param site: site is the string with site abbreviation
        :return: BeautifulSoup object of the site where the score is on
        """
        with requests.Session() as crawl_session:
            if site in login_urls:  # you need to login to access points
                crawl_session.post(login_urls[site], credentials.ht)

            # get the profile page where the scores are on
            request = crawl_session.get(self.profile_url)
            request.raise_for_status()

            request_content = request.content
            return BeautifulSoup(request_content, "html.parser")  # convert to BeautifulSoup response

    def get_score(self):
        """
        Gets score from BeautifulSoup object
        :return: exact score that the user has on the site
        :rtype: int
        """
        response = self.get_page_content(self.site)
        if not 'User not found' in str(response):
            spans = response.find_all("span", class_="right")
            score = spans[0].contents[0]
        else:  # It would take the score of the user logged in when the user was not found.
            raise AccountDoesNotExist(self.site, self.username)
        return int(score)
