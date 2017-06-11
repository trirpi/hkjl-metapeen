from basecrawler import BaseCrawler, AccountDoesNotExist
import re


class HTSCrawler(BaseCrawler):
    """Crawler for hackthissite.org."""
    site = 'hts'

    def get_score(self):
        """
        Gets score from BeautifulSoup object
        :return: exact score that the user has on the site
        :rtype: int
        """
        response = self.get_page_content(self.site)
        try:
            score_element = response.find_all('td', class_='blight-td')[1]
            score = re.findall(r'\d+', str(score_element.contents[0]))[0]
        except IndexError:
            raise AccountDoesNotExist(self.site, self.username)
        return int(score)
