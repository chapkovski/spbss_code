from otree.api import *

doc = """
Dictator game
"""


class Constants(BaseConstants):
    name_in_url = 'dg'
    players_per_group = 2
    num_rounds = 1
    dictator_role = 'Participant A'
    recipient_role = 'Participant B'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class Instructions(Page):
    pass


class Decision(Page):
    @staticmethod
    def is_displayed(player):
        return player.role == Constants.dictator_role


class Belief(Page):
    @staticmethod
    def is_displayed(player):
        return player.role == Constants.recipient_role


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [
    Instructions,
    Decision,
    Belief,
    ResultsWaitPage,
    Results
]
