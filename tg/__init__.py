from otree.api import *




doc = """
This is a standard 2-player trust game where the amount sent by player 1 gets
tripled. 
Berg J, Dickhaut J, McCabe K. Trust, reciprocity, and social history. Games and economic behavior. 1995 Jul 1;10(1):122-42.
</a>.
"""


class Constants(BaseConstants):
    name_in_url = 'trust'
    players_per_group = 2
    num_rounds = 1
    instructions_template = 'tg/includes/instructions.html'
    # Initial amount allocated to each player
    endowment = cu(100)
    multiplier = 3
    sender_role = 'Participant A'
    receiver_role = 'Participant B'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    sent_amount = models.CurrencyField(
        min=0,
        max=Constants.endowment,

        label=f"Please enter an amount from 0 to {Constants.endowment}:",
    )
    tripled_amount = models.CurrencyField( )
    sent_back_amount = models.CurrencyField( min=cu(0))


class Player(BasePlayer):
    pass


# FUNCTIONS
def sent_back_amount_max(group: Group):
    return group.sent_amount * Constants.multiplier


def set_payoffs(group: Group):
    sender = group.get_player_by_role(Constants.sender_role)
    receiver = group.get_player_by_role(Constants.receiver_role)
    sender.payoff = Constants.endowment - group.sent_amount + group.sent_back_amount
    receiver.payoff = group.sent_amount * Constants.multiplier - group.sent_back_amount


# PAGES
class Introduction(Page):
    pass


class Send(Page):
    """This page is only for Sender
    Sender sends amount (all, some, or none) to Receiver
    This amount is tripled by experimenter,
    i.e if sent amount by P1 is 5, amount received by Receiver is 15"""

    form_model = 'group'
    form_fields = ['sent_amount']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == Constants.sender_role

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.group.tripled_amount = player.group.sent_amount * Constants.multiplier
class SendBackWaitPage(WaitPage):
    pass


class SendBack(Page):
    """This page is only for P2
    P2 sends back some amount (of the tripled amount received) to P1"""

    form_model = 'group'
    form_fields = ['sent_back_amount']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == Constants.receiver_role




class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    """This page displays the earnings of each player"""



page_sequence = [
    Introduction,
    Send,
    SendBackWaitPage,
    SendBack,
    ResultsWaitPage,
    Results,
]
