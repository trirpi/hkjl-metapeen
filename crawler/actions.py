from peen import db

from crawler.cs_crawler import CSCrawler
from crawler.ht_crawler import HTCrawler
from crawler.otw_crawler import OTWCrawler
from crawler.rm_crawler import RMCrawler
from crawler.hts_crawler import HTSCrawler
from crawler.nf_crawler import NFCrawler

crawler_classes = {
    'cs': CSCrawler,
    'otw': OTWCrawler,
    'ht': HTCrawler,
    'rm': RMCrawler,
    'hts': HTSCrawler,
    'nf': NFCrawler,
}


def update_score(hacker, short_site_name):
    """
    Update score of a user of a specific site
    :param hacker: hacker class instance
    :param short_site_name: site abbreviation like 'rm'
    :return: 
    """
    try:
        crawler = crawler_classes[short_site_name](hacker)  # create crawler instance for specific user
        score = crawler.get_score()  # get score

        hacker.update_score(short_site_name, score)  # set new values
        db.session.commit()
    except KeyError:  # if the site is not valid
        print('[*] Error: The site ' + short_site_name.full_name + ' from user ' + hacker.username + ' does not exist.')


def update_all_scores(hacker):
    """
    Update scores of a user.
    :param hacker: person whose score should be updated
    :type hacker: Hacker class instance
    :return: None

    :Example:

    >>> from peen.models import Hacker
    >>> hacker = Hacker.query.filter_by(username='henk').first()
    >>> update_all_scores(hacker)
    """

    for account in hacker.accounts.all():
        update_score(hacker, account.short_site_name)


def update_total_score(hacker):
    hacker.update_total_score()
