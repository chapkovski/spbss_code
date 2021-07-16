from otree.api import *

doc = """
Dice game 
Fischbacher U, Föllmi-Heusi F. Lies in disguise—an experimental study on cheating. Journal of the European Economic Association. 2013 Jun 1;11(3):525-47.

"""


class Constants(BaseConstants):
    name_in_url = 'dice'
    players_per_group = None
    num_rounds = 1
    payoffs = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 0}


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    answer = models.IntegerField(min=1, max=6)
    belief = models.FloatField(min=1, max=6)


def set_payoff(player, timeout_happened):
    player.payoff = Constants.payoffs[player.answer]


# PAGES
class Intro(Page):
    pass


class Decision(Page):
    form_model = 'player'
    form_fields = ['answer']
    before_next_page = set_payoff


class Belief(Page):
    form_model = 'player'
    form_fields = ['belief']

    @staticmethod
    def is_displayed(player: Player):
        return player.session.config.get('beliefs', False)


class Results(Page):
    pass


page_sequence = [
    Intro,
    Decision,
    Belief,
    Results
]
