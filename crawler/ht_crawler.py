from crawler.basecrawler import BaseCrawler


class HTCrawler(BaseCrawler):
    """Crawler for hackthis.co.uk."""
    site = 'ht'

    def get_score(self):
        """
        Gets score from BeautifulSoup object
        :return: exact score that the user has on the site
        :rtype: int
        """
        response = self.get_page_content(self.site)

        spans = response.find_all("span", class_="right")
        score = spans[0].contents[0]
        return int(score)