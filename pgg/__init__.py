from otree.api import *



class Constants(BaseConstants):
    name_in_url = 'pgg'
    players_per_group = 3
    num_rounds = 1
    endowment = cu(100)
    multiplier = 1.8


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()


class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=0, max=Constants.endowment, label=f"How much will you contribute (from 0 to {Constants.endowment} points)?"
    )


# FUNCTIONS
def set_payoffs(group: Group):
    players = group.get_players()
    contributions = [p.contribution for p in players]
    group.total_contribution = sum(contributions)
    group.individual_share = (
        group.total_contribution * Constants.multiplier / Constants.players_per_group
    )
    for p in players:
        p.payoff = Constants.endowment - p.contribution + group.individual_share


# PAGES
class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    pass


page_sequence = [
    Contribute,
    ResultsWaitPage,
    Results
]
