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
        if not 'User not found' in str(response):
            spans = response.find_all("span", class_="right")
            score = spans[0].contents[0]
        else:  # It would take the score of the user logged in when the user was not found.
            print('[*] Info: User ' + self.username + ' does not have an account on hackthis.')
            score = 0
        return int(score)
