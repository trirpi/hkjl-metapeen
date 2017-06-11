from basecrawler import BaseCrawler, AccountDoesNotExist
import re


class NFCrawler(BaseCrawler):
    """Crawler for net-force.nl."""
    site = 'nf'

    def get_score(self):
        """
        Gets score from BeautifulSoup object
        :return: exact score that the user has on the site
        :rtype: int
        """
        response = self.get_page_content(self.site)

        try:
            score = re.findall(r'\d+', response.find_all("span")[0].text)[0]
        except IndexError:
            raise AccountDoesNotExist(self.site, self.username)
        return int(score)
