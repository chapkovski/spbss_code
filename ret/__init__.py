from otree.api import *
import random
from otree.database import db
doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'ret'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


class Task(ExtraModel):
    player = models.Link(Player)
    first = models.IntegerField()
    second = models.IntegerField()
    correct_answer = models.IntegerField()
    answer = models.IntegerField()
    is_correct= models.BooleanField()

# PAGES
class TaskPage(Page):
    timeout_seconds = 30

    @staticmethod
    def live_method(player, data):
        print('received data from', player.id_in_group, ':', data)
        answer = data.get('answer')
        task_id = data.get('task_id')
        if answer and task_id:
            t= Task.objects_get(id = task_id)
            t.answer = answer
            t.answer = answer
            t.is_correct = answer == t.correct_answer


        first = random.randint(100, 999)
        second = random.randint(100, 999)
        correct_answer = first+second
        task = Task.create(player=player,
                           first=first,
                           second=second,
                           correct_answer=correct_answer)
        db.commit()
        return {player.id_in_group: dict(first=first,
                                         second=second, task_id=task.id)}


class Results(Page):
    pass


page_sequence = [TaskPage, Results]
def custom_export(players):
    # header row
    yield ['task_id', 'first', 'second', 'answer', 'correct answer', 'is correct', 'participant', 'session']
    for p in players:
        tasks = db.query(Task).filter(Task.answer.isnot(None)).all()
        for t in tasks:
            participant = p.participant
            session = p.session
            yield [t.id, t.first, t.second, t.answer, t.correct_answer, t.is_correct, participant.code,session.code,]