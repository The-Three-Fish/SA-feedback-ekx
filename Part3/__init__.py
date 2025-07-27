from otree.api import *
import random
import csv

author = 'Lingguo XU'
doc = """
Part 3
"""

class Constants(BaseConstants):
    name_in_url = 'Part3'
    players_per_group = None
    ECUpercorrect = 30

    with open('Part3/Part4_asnwerkey.csv') as questions_file:
        questions = list(csv.DictReader(questions_file))

    # num_rounds = len(questions)
    num_rounds = 20

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
    wta_t2 = models.IntegerField(min=600, max=750, label="Please put in the minimum price you are willing to sell.")

    solution = models.StringField()
    task_answers = models.StringField(choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            label="Please select a number.", initial="")
    is_correct = models.BooleanField(initial=0)

    def current_question(player):
        return player.session.vars['questions'][player.round_number - 1]

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
class ReadyTask_ASU(Page):
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
            participant.is_dropout = False

        import time
        # user has 10 minutes to complete as many pages as possible
        participant.vars['expiry'] = time.time() + player.session.config['task_round_timeout_seconds']

class Task(Page):
    form_model = 'player'
    form_fields = ['task_answers']
    timer_text = 'Time left:'
    # timeout_seconds = 20

    get_timeout_seconds = get_timeout_seconds

    @staticmethod
    def is_displayed(player):
        return player.participant.is_dropout == False

    @staticmethod
    def vars_for_template(player):
        return dict(
            image_path_1='Part4/ImagQuestions/{}.png'.format(player.round_number),
            image_path_2='Part4/ImagAnswers/{}.png'.format(player.round_number),
            round_number = player.round_number
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        import time

        if player.task_answers:
            player.is_correct = (player.task_answers.lower() == player.solution.lower())

    @staticmethod
    def error_message(player, value):
        print('You typed in', value)
        if value['task_answers'] not in ["a", "b", "c", "d", "e", "f"]:
            return 'Please enter a single lower-case letter, from the a list of "a", "b", "c", "d", "e", and "f".'

class Results_t1(Page):
    def is_displayed(player):
        return player.round_number == Constants.num_rounds and player.participant.treatment == 1

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
            participant.is_dropout = False

class Results_t2(Page):
    form_model = 'player'
    form_fields = ['wta_t2']

    def is_displayed(player):
        return player.round_number == Constants.num_rounds and player.participant.treatment == 2

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

        participant = player.participant

        participant.wta_t2 = player.wta_t2

        participant.buyer_price = random.choice(range(600, 750))

        if participant.wta_t2 >= participant.buyer_price:
            participant.get_gold = 1
            participant.gold_payment = participant.gold_value
        else:
            participant.get_gold = 0
            participant.gold_payment = participant.wta_t2

class T2_reveal(Page):
    def is_displayed(player):
        return player.round_number == Constants.num_rounds and player.participant.treatment == 2

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
            participant.is_dropout = False

page_sequence = [ReadyTask_ASU, Task, Results_t1, Results_t2, T2_reveal]