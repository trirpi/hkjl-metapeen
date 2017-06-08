from crawler.basecrawler import BaseCrawler, AccountDoesNotExist
import re


class CSCrawler(BaseCrawler):
    """Crawler for certifiedsecure.com."""
    site = 'cs'

    def get_score(self):
        """
        Gets score from BeautifulSoup object
        :return: exact score that the user has on the site
        :rtype: int
        """
        response = self.get_page_content(self.site)
        try:
            score = re.findall(r'\d+', response.find_all("div", class_="level_progress_details")[0].text)[1]
        except IndexError:
            raise AccountDoesNotExist
        return int(score)