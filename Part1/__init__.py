from otree.api import *
import random
import csv

author = 'Lingguo Xu'
doc = """
Part 1: Attention pledge, PLS, overview, instructions for game and task. Same for all treatments
"""

class Constants(BaseConstants):
    name_in_url = 'Part1'
    players_per_group = None
    num_rounds = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    consent = models.IntegerField(label="",
        choices=[[1, 'I agree']],
        widget=widgets.RadioSelect
    )

    sign_yesno = models.IntegerField(
        choices=[
            [1, 'Yes, I would like to see the pan'],
            [0, 'No, I do not wish see the pan'],
        ],
        widget = widgets.RadioSelect,
        label = ""
    )

    def make_field_WTP():
        return models.IntegerField(label="Please fill in a number between 0 and 50")

    # WTP for advance information
    sign_wtp = make_field_WTP()

    bdm = models.IntegerField(
        choices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        label = "Please select the a number"
    )

# FUNCTIONS
def creating_session(subsession):
    for player in subsession.get_players():
        player.participant.is_dropout = False
        print('set player.participant.is_dropout', player.participant.is_dropout)
        player.participant.treatment  = player.session.config['treatment']

# PAGES
class Attention_pledge(Page):
    pass

class PLS_Consent(Page):
    form_model = 'player'
    form_fields = ['consent']

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

class Part0_waitpage_ASU(Page):
    def is_displayed(player):
        return player.participant.is_dropout == False

    @staticmethod
    def get_timeout_seconds(player):
        participant = player.participant

        if participant.is_dropout:
            return 1  # instant timeout, 1 second
        else:
            return player.session.config['my_page_timeout_seconds']

    # Manually advance players in this page, does not consider as dropout
    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant

        if timeout_happened:
            participant.is_dropout = False

class Overview_ASU(Page):
    def is_displayed(player):
        return player.participant.is_dropout == False

    @staticmethod
    def get_timeout_seconds(player):
        participant = player.participant

        if participant.is_dropout:
            return 1  # instant timeout, 1 second
        else:
            return player.session.config['my_page_timeout_seconds']

    # Manually advance players in this page, does not consider as dropout
    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant

        if timeout_happened:
            participant.is_dropout = False

class BDM(Page):
    form_model = 'player'
    form_fields = ['bdm']

    def is_displayed(player):
        return player.participant.is_dropout == False

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

class Instruction1(Page):
    def is_displayed(player):
        return player.participant.is_dropout == False

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

class Instruction2(Page):

    def is_displayed(player):
        return player.participant.is_dropout == False

    # @staticmethod
    # def error_message(player, value):
    #     print('You typed in', value)
    #     if value['practice1'] not in ["a", "b", "c", "d", "e", "f"]:
    #         return 'Please enter a single lower-case letter, from the a list of "a", "b", "c", "d", "e", and "f".'

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

class Instruction3(Page):

    form_model = 'player'
    form_fields = ['sign_wtp']

    def is_displayed(player):
        return player.participant.is_dropout == False

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

        # participant.advance_info = (player.sign_wtp != 0)
        player.participant.advance_info_wtp = player.sign_wtp

        if random.choice(range(0, 10000000000000)) > 0:
            player.participant.miner_price = 0
        else:
            player.participant.miner_price = random.choice(range(1, 50))

        if player.sign_wtp >= player.participant.miner_price:
            player.participant.advance_info = 1
        else:
            player.participant.advance_info = 0

class sign_wtp(Page):
    pass

page_sequence = [Overview_ASU, sign_wtp]
# page_sequence = [Attention_pledge, PLS_Consent, Overview_ASU, BDM, Instruction1, Instruction2, Instruction3, sign_wtp]
