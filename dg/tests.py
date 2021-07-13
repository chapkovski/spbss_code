from otree.api import Currency as c, currency_range, expect, Bot
from . import *
import random


class PlayerBot(Bot):
    def play_round(self):
        yield Intro,
        if self.player.role ==Constants.dictator_role:
            yield Decision, dict(send=random.randint(0, Constants.endowment))
        if self.player.role == Constants.recipient_role:
            yield Belief, dict(belief=random.randint(0, Constants.endowment))

        yield Results
