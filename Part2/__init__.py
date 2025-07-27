from otree.api import *
import random

author = 'Lingguo XU'
doc = """
Part 2: belief elicitations
"""

class Constants(BaseConstants):
    name_in_url = 'Part2'
    players_per_group = None
    num_rounds = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    # Absolute belief and confidence on belief
    wta_t1  = models.IntegerField(min=600, max=750, label="Please put in the minimum price you are willing to sell")

    # random_broke = models.BooleanField() # Indicator variable for those whose correct answers are on the break point (12, 16, 19, 22 for 100 subjects in Pilot 1 & 2)
    # bef_rel_real = models.IntegerField() # The percentage subjects assigned to his real relative performance interval
    # # bef_rel_real_Pilot2 = models.IntegerField() # The percentage subjects assigned to his real relative performance interval, ranking based on data from Pilot 2
    #
    # bsr_random_interval = models.IntegerField() # pick a random interval which will be used to determine whether subjects receive reward or not
    # bsr_t = models.IntegerField() # = 100 if bsr_random_interval = real_rel
    # bsr_p = models.IntegerField() # The percentage subjects assigned to the interval randomly drew by the computer
    # bsr_penalty = models.IntegerField() # Chances of receiving reward according to BSR
    # bsr_n = models.IntegerField() # pick a random number which will be used to determine whether subjects receive reward or not
    # bsr_payment = models.IntegerField() # payment from bef_rel question based on BSR
    # bsr_clicked = models.BooleanField(initial = 0)

    #Payoff for Part 2
    payoff_part2 = models.IntegerField()

# FUNCTIONS

def creating_session(subsession):
    for player in subsession.get_players():
        player.participant.gold_value = random.choice(range(600, 750))
        print('set player.participant.gold_value', player.participant.gold_value)

# PAGE
class T1_wta (Page):
    form_model = 'player'
    form_fields = ['wta_t1']

    def is_displayed(player):
        return player.participant.treatment == 1

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

        participant.wta_t1 = player.wta_t1

        participant.buyer_price = random.choice(range(600, 750))

        if participant.wta_t1 >= participant.buyer_price:
            participant.get_gold = 1
            participant.gold_payment = participant.gold_value
        else:
            participant.get_gold = 0
            participant.gold_payment = participant.wta_t1

class T1_reveal(Page):
    form_model = 'player'

    # def is_displayed(player):
    #     return player.participant.is_dropout == False

    def is_displayed(player):
        return player.participant.treatment == 1

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

class T2_delay(Page):
    form_model = 'player'

    def is_displayed(player):
        return player.participant.treatment == 2

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


page_sequence = [T1_wta, T1_reveal, T2_delay]
# page_sequence = [EndPage_ASU]


