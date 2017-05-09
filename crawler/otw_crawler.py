from crawler.basecrawler import BaseCrawler
import re


class OTWCrawler(BaseCrawler):
    """Crawler for overthewire.org."""
    site = 'otw'

    def get_score(self):
        """
        Gets score from BeautifulSoup object
        :return: exact score that the user has on the site
        :rtype: int
        """
        response = self.get_page_content(self.site)

        table = response.find_all("table")[1]
        for words in table.contents:  # loop over tables to find the overthewire table where the correct score is stored
            if 'OverTheWire.org' in str(words):
                return int(re.findall(r'\d+', str(words.contents[2]))[0])
