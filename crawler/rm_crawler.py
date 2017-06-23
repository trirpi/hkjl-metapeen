from crawler.basecrawler import BaseCrawler, AccountDoesNotExist


class RMCrawler(BaseCrawler):
    """Crawler for root-me.org."""
    site = 'rm'

    def get_score(self):
        """
        Gets score from BeautifulSoup object
        :return: exact score that the user has on the site
        :rtype: int
        """
        response = self.get_page_content(self.site)
        try:
            score = response.find_all("div", class_="t-body")[0].contents[5].contents[5].contents[1].text
        except IndexError:
            raise AccountDoesNotExist(self.site, self.username)
        return int(score)
