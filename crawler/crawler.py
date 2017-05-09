from peen import db

from crawler.cs_crawler import CSCrawler
from crawler.ht_crawler import HTCrawler
from crawler.otw_crawler import OTWCrawler
from crawler.rm_crawler import RMCrawler
from crawler.hts_crawler import HTSCrawler

crawler_callbacks = {
    'cs': CSCrawler,
    'otw': OTWCrawler,
    'ht': HTCrawler,
    'rm': RMCrawler,
    'hts': HTSCrawler
}


def update_score(hacker, site=None):
    """
    Update scores of a user.
    :param hacker: person whose score should be updated
    :type hacker: Hacker class instance
    :param site: site that needs to be updated (if none it updates all scores)
    :return: None

    :Example:

    >>> from peen.orm.models import Hacker
    >>> hacker = Hacker.query.filter_by(username='henk').first()
    >>> update_score(hacker, site='rm')
    """
    scores = hacker.scores  # list with username/id and current score
    username = hacker.username

    if site is None:  # update scores of all sites the user has
        for site_key in scores:
            crawler = crawler_callbacks[site_key](username)  # create crawler instance for specific user
            score = crawler.get_score()  # get score

            hacker.update_score(site_key, score)  # set new values
    else:  # update the specific site
        crawler = crawler_callbacks[site](username)  # create crawler instance for specific user with the correct site
        score = crawler.get_score()  # get score

        hacker.update_score(site, score)  # set new values

    db.session.commit()  # and put them in the db