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


def update_score(hacker, site):
    """
    Update score of a user of a specific site
    :param hacker: hacker class instance
    :param site: site abbreviation like 'rm'
    :return: 
    """
    try:
        crawler = crawler_classes[site](hacker)  # create crawler instance for specific user
        score = crawler.get_score()  # get score

        hacker.update_score(site, score)  # set new values
        db.session.commit()
    except KeyError:  # if the site is not valid
        print('[*] Error: The site ' + site + ' from user ' + hacker.username + ' does not exist.')


def update_all_scores(hacker):
    """
    Update scores of a user.
    :param hacker: person whose score should be updated
    :type hacker: Hacker class instance
    :return: None

    :Example:

    >>> from peen.orm.models import Hacker
    >>> hacker = Hacker.query.filter_by(username='henk').first()
    >>> update_all_scores(hacker)
    """

    for site_name in hacker.get_site_names():
        update_score(hacker, site_name)


def update_total_score(hacker):
    hacker.update_total_score()
