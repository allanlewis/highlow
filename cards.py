# coding=utf-8
import logging
import textwrap
from collections import defaultdict
from functools import total_ordering

import certifi
import urllib3
from apiclient import APIClient

DECK_OF_CARDS_BASE_URL = 'http://deckofcardsapi.com/api/deck/'

logger = logging.getLogger(__name__)


class MyAPIClient(APIClient):

    POOL_MANAGER = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',  # Force certificate check.
        ca_certs=certifi.where(),  # Path to the Certifi bundle.
    )

    def __init__(self, rate_limit_lock=None):
        super(MyAPIClient, self).__init__(rate_limit_lock)

    def _make_connection_pool(self, url):
        return self.POOL_MANAGER.connection_from_url(url)

    def call(self, path, **params):
        response = super(MyAPIClient, self).call(path, **params)
        logger.debug(response)
        return response


class CardsClient(MyAPIClient):
    BASE_URL = DECK_OF_CARDS_BASE_URL

    def shuffle(self, deck_count=1):
        response = self.call('new/shuffle/', deck_count=deck_count)
        return response['deck_id']

    def draw(self, deck_id='new', count=1):
        response = self.call('{}/draw/'.format(deck_id), count=count)
        return response['cards']

    def draw_one(self, deck_id='new'):
        return self.draw(deck_id)[0]


@total_ordering
class Card(object):

    ASCII = textwrap.dedent("""
        ┌─────────┐
        │{}       │
        │         │
        │         │
        │    {}   │
        │         │
        │         │
        │       {}│
        └─────────┘
        """.format('{value[0]: <2}', '{suit_icon: <4}', '{value[0]: >2}'))
    SUITS = {'CLUBS': '♣', 'DIAMONDS': '♦', 'HEARTS': '♥', 'SPADES': '♠'}
    VALUES = {str(s): s for s in range(2, 11)}
    VALUES['JACK'] = 11
    VALUES['QUEEN'] = 12
    VALUES['KING'] = 13
    VALUES['ACE'] = 1

    def __init__(self, image, value, suit, code, **_):
        self.image, self.value, self.suit, self.code = image, value, suit, code
        self.suit_icon = self.SUITS[suit]

    def __eq__(self, other):
        return self.VALUES[self.value] == self.VALUES[other.value]

    def __lt__(self, other):
        return self.VALUES[self.value] < self.VALUES[other.value]

    def __str__(self):
        return self.ASCII.format(**self.__dict__)

if __name__ == '__main__':
    print Card(None, 'KING', 'HEARTS', None)
