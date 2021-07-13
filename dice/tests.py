from otree.api import Currency as c, currency_range, expect, Bot
from . import *
import random


class PlayerBot(Bot):
    def play_round(self):
        yield Intro,
        yield Decision, dict(answer=random.randint(1, 6))
        if self.session.config.get('beliefs'):
            yield Belief, dict(belief=random.randint(1, 6))
        yield Results
