from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Instructions(Page):
    def vars_for_template(self):
        self.player.treatment = self.player.participant.vars['treatment']
        return {
            'treatment': self.player.treatment,
        }


class Task(Page):
    timeout_seconds = Constants.time_limit
    form_model = 'player'
    def get_form_fields(self):
            return ['anagram_' + str(j) for j in range(1, Constants.total_number + 1)]

    def vars_for_template(self):
        return {
           'treatment': self.participant.vars['treatment'],
           'words_select_easy': self.participant.vars['words_select_easy'],
           'words_select_difficult': self.participant.vars['words_select_difficult'],
           'anagram_select_easy': self.participant.vars['anagram_select_easy'],
           'anagram_select_difficult': self.participant.vars['anagram_select_difficult'],
           'pair_select_easy': self.participant.vars['pair_select_easy'],
           'pair_select_difficult': self.participant.vars['pair_select_difficult']
        }

    def before_next_page(self):
        self.player.check_correct()


class Results(Page):
    pass

page_sequence = [
    Instructions,
    Task,
    Results
]
