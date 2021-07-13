from otree.api import *

doc = """
One player decides how to divide a certain amount between himself and the other
player.
See: Kahneman, Daniel, Jack L. Knetsch, and Richard H. Thaler. "Fairness
and the assumptions of economics." Journal of business (1986):
S285-S300.
"""


class Constants(BaseConstants):
    name_in_url = 'dictator'
    players_per_group = 2
    num_rounds = 1
    instructions_template = 'dictator/instructions.html'
    # Initial amount allocated to the dictator
    endowment = cu(100)
    dictator_role = 'Participant A'
    recipient_role = 'Participant B'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    send = models.CurrencyField(
        doc="""Amount dictator sends to a Recipient""",
        min=0,
        max=Constants.endowment,
        label=f"I will send to {Constants.recipient_role}",
    )
    kept = models.CurrencyField()
    belief = models.CurrencyField()


class Player(BasePlayer):
    pass


# FUNCTIONS
def set_payoffs(group: Group):
    dictator = group.get_player_by_role(Constants.dictator_role)
    recipient = group.get_player_by_role(Constants.recipient_role)
    group.kept = Constants.endowment - group.send
    dictator.payoff = group.kept
    recipient.payoff = group.send


# PAGES
class Intro(Page):
    pass


class Decision(Page):
    form_model = 'group'
    form_fields = ['send']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == Constants.dictator_role


class Belief(Page):
    form_model = 'group'
    form_fields = ['belief']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == Constants.recipient_role


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    pass


page_sequence = [
    Intro,
    Decision,
    Belief,
    ResultsWaitPage,
    Results
]
