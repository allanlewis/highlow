import cmd
import logging

import operator

from cards import Card, CardsClient

LOG_FORMAT = '%(asctime)s [%(name)-22s] %(levelname)-8s: %(message)s'
LOG_LEVEL = logging.WARNING

logger = logging.getLogger(__name__)


# noinspection PyMethodMayBeStatic
class HighLow(cmd.Cmd):
    def __init__(self, completekey='tab', stdin=None, stdout=None):
        cmd.Cmd.__init__(self, completekey, stdin, stdout)
        self.cards = CardsClient()
        self.deck_id = self.cards.shuffle()
        self.current_card = None

    def draw_one(self):
        card = Card(**self.cards.draw_one(self.deck_id))
        print card
        return card

    def cmdloop(self, intro=None):
        self.current_card = self.draw_one()
        cmd.Cmd.cmdloop(self, intro)

    def _do_higher_lower(self, compare):
        new_card = self.draw_one()
        if compare(self.current_card, new_card):
            print 'You lose!'
            return True
        self.current_card = new_card
        print 'Well done!'

    def do_higher(self, *_):
        return self._do_higher_lower(operator.gt)

    def do_lower(self, *_):
        return self._do_higher_lower(operator.lt)

    def do_EOF(self, *_):
        """Exit on new-line."""
        return True

    def do_foo(self, line):
        print self, 'doing foo', line

if __name__ == '__main__':
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
    logging.getLogger('cards').setLevel(logging.DEBUG)
    HighLow().cmdloop()
