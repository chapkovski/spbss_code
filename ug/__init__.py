from otree.api import *
import random

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'ultimatum'
    players_per_group = 2
    num_rounds = 1
    proposer_role = 'Proposer'
    responder_role = 'Responder'
    instructions_template = 'ug/includes/instructions.html'
    endowment = cu(100)
    payoff_if_rejected = cu(0)
    offer_increment = cu(10)
    offer_choices = currency_range(0, endowment, offer_increment)
    offer_choices_count = len(offer_choices)
    keep_give_amounts = []
    for offer in offer_choices:
        keep_give_amounts.append((offer, endowment - offer))




class Subsession(BaseSubsession):
    pass


def question(amount):
    return 'Would you accept an offer of {}?'.format(cu(amount))

def make_field(label):
    return models.BooleanField(
        choices=[[False, 'No'], [True, 'Yes']],
        label=label,
        widget=widgets.RadioSelect,
    )

class Group(BaseGroup):
    strategy = models.BooleanField(
        doc="""Whether this group uses strategy method""",

    )

    amount_offered = models.CurrencyField(choices=Constants.offer_choices,
                                          widget=widgets.RadioSelect,
                                          label=f'How much you would like to offer to  {Constants.responder_role}?'
                                          )

    offer_accepted = models.BooleanField(
        doc="if offered amount is accepted (direct response method)",
        label=f'Do you want to accept this offer made by {Constants.proposer_role}?'
    )

    # for strategy method
    response_0 = make_field(question(0))
    response_10 = make_field(question(10))
    response_20 = make_field(question(20))
    response_30 = make_field(question(30))
    response_40 = make_field(question(40))
    response_50 = make_field(question(50))
    response_60 = make_field(question(60))
    response_70 = make_field(question(70))
    response_80 = make_field(question(80))
    response_90 = make_field(question(90))
    response_100 = make_field(question(100))


class Player(BasePlayer):
    pass

def creating_session(subsession:Subsession):
    # randomize to treatments
    for g in subsession.get_groups():
        if 'strategy' in subsession.session.config:
            g.strategy = subsession.session.config['strategy']
        else:
            g.strategy = random.choice([True, False])


def set_payoffs(group: Group):
    proposer = group.get_player_by_role(Constants.proposer_role)
    responder = group.get_player_by_role(Constants.responder_role)

    if group.strategy:
        group.offer_accepted = getattr(group, 'response_{}'.format(
            int(group.amount_offered)))

    if group.offer_accepted:
        proposer.payoff = Constants.endowment - group.amount_offered
        responder.payoff = group.amount_offered
    else:
        responder.payoff = Constants.payoff_if_rejected
        proposer.payoff = Constants.payoff_if_rejected

# PAGES
class Introduction(Page):
    timeout_seconds = 600


class Offer(Page):
    form_model = 'group'
    form_fields = ['amount_offered']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == Constants.proposer_role

class WaitForProposer(WaitPage):
    pass


class Accept(Page):
    form_model = 'group'
    form_fields = ['offer_accepted']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == Constants.responder_role and not player.group.strategy




class AcceptStrategy(Page):
    form_model = 'group'
    form_fields = ['response_{}'.format(int(i)) for i in
                   Constants.offer_choices]

    @staticmethod
    def is_displayed(player: Player):
        return player.role == Constants.responder_role and player.group.strategy


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    pass


page_sequence = [
    Introduction,
    Offer,
    WaitForProposer,
    Accept,
    AcceptStrategy,
    ResultsWaitPage,
    Results
]
