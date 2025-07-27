from otree.api import *
import random
import csv

author = 'Lingguo XU'
doc = """
Part 1: first task round
"""

class Constants(BaseConstants):
    name_in_url = 'Task1'
    players_per_group = None
    ECUpercorrect = 40

    with open('Task1/asnwerkey.csv') as questions_file:
        questions = list(csv.DictReader(questions_file))

    # num_rounds = len(questions)
    num_rounds = 30

class Subsession(BaseSubsession):
    def creating_session(subsession):
        if player.round_number == 1:
            player.session.vars['questions'] = Constants.questions.copy()

        for player in subsession.get_players():
            question_data = current_question(player)
            player.solution = question_data['solution']
            player.round_number = player.round_number


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    solution = models.StringField()
    task_answers = models.StringField(label="Your answer", initial="")
    is_correct = models.BooleanField(initial=0)

    def current_question(player):
        return player.session.vars['questions'][player.round_number - 1]

    num_checks = models.IntegerField(initial=0, blank = True)
    timeonimage = models.FloatField(initial=0, blank = True)

# FUNCTIONS
def get_timeout_seconds(player):
    import time
    return player.participant.expiry - time.time()

def creating_session(subsession):
    for player in subsession.get_players():
        if player.round_number == 1:
            player.session.vars['questions'] = Constants.questions.copy()

        question_data = player.current_question()
        player.solution = question_data['solution']
        player.round_number = player.round_number

# PAGES
class ReadyTask(Page):

    def is_displayed(player):
        return player.participant.is_dropout == False and player.round_number == 1

    @staticmethod
    def get_timeout_seconds(player):
        participant = player.participant

        if participant.is_dropout:
            return 1  # instant timeout, 1 second
        else:
            return player.session.config['my_page_timeout_seconds']

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant

        if timeout_happened:
            participant.is_dropout = True

        import time
        # user has 10 minutes to complete as many pages as possible
        participant.vars['expiry'] = time.time() + player.session.config['task_round_timeout_seconds']

class Task(Page):

    form_model = 'player'
    form_fields = ['task_answers', 'num_checks', 'timeonimage']
    timer_text = 'Time left:'
    # timeout_seconds = 20

    get_timeout_seconds = get_timeout_seconds

    @staticmethod
    def is_displayed(player):
        return player.participant.is_dropout == False

    @staticmethod
    def vars_for_template(player):
        return dict(
            image_path_1='Part1/ImagQuestions/{}.png'.format(player.round_number),
            image_path_2='Part1/ImagAnswers/{}.jpg'.format(player.round_number),
            round_number = player.round_number
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        import time

        if player.task_answers:
            player.is_correct = (player.task_answers.lower() == player.solution.lower())

    # @staticmethod
    # def error_message(player, value):
    #     print('You typed in', value)
    #     if value['task_answers'] not in ["0", "1", "2", "3", "4", "5", "6", "7", "8"]:
    #         return 'Please enter a single digit number.'

    @staticmethod
    def js_vars(player):
        return dict(
            roundnum = player.round_number,
        )

class Results_ASU(Page):

    @staticmethod
    def is_displayed(player):
        return player.round_number == Constants.num_rounds and player.participant.is_dropout == False

    @staticmethod
    def get_timeout_seconds(player):
        if player.participant.is_dropout:
            return 1  # instant timeout, 1 second
        else:
            return player.session.config['my_page_timeout_seconds']

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.participant.is_dropout = False

page_sequence = [ReadyTask, Task, Results_ASU]