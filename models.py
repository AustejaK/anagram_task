from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

author = 'Austėja Kažemekaitytė'

doc = """
An example of an effort task, where a participant has to solve a list of anagrams. This task includes two treatments:
easy anagrams and difficult anagrams. The task has a time limit of 5 minutes.
"""


class Constants(BaseConstants):
    name_in_url = 'anagram_task'
    players_per_group = None
    num_rounds = 1
    # Create a list of words and their anagrams
    word_list_easy = ["hazel", "whale", "width", "frown", "stand", "guard", "train", "query", "viper", "choir", "match",
                      "chair", "child", "logic", "clown", "brown", "cloud", "fancy", "joker", "rough"]

    word_list_difficult = ["gular", "jorum", "tumid", "tagma", "numen", "oribi", "epode", "roshi", "sapid", "roily",
                           "apeak", "gigue", "besom", "cover", "papaw", "vicar", "aioli", "force", "lurid", "pasha"]

    anagram_list_easy = ["azhle", "lwahe", "htiwd", "rnowf", "nadts", "augrd", "nrtai", "yqeru", "ivper", "hcoir",
                         "hactm", "ciahr", "dhilc", "ioglc", "ownlc", "wnobr", "ldouc", "acnfy", "erjko", "ougrh"]

    anagram_list_difficult = ["laurg", "rmjuo", "miudt", "agtam", "eunnm", "iibro", "dpeeo", "isorh", "iapsd", "iylor",
                              "epkaa", "uiegg", "smbeo", "verco", "ppaaw", "criav", "iiola", "ofrec", "iurdl", "sphaa"]

    total_number = len(word_list_easy)
    # Bonus payment for each correct solution of an anagram
    bonus = c(0.02)
    # Time limit for solving all the anagrams
    time_limit = 200
    # Matching each word and a corresponding anagram in a list
    tabs = list(range(1, total_number + 1))
    pair_list_easy = list(zip(word_list_easy, anagram_list_easy, tabs))
    pair_list_difficult = list(zip(word_list_difficult, anagram_list_difficult, tabs))

class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            for p in self.get_players():
                # This version has two treatments: easy anagrams and difficult anagrams
                p.participant.vars['treatment'] = random.choice(['easy', 'difficult'])
                indices = [j for j in range(1, Constants.total_number + 1)]
                anagram_choice = ['anagram_' + str(j) for j in range(1, Constants.total_number + 1)]
                word_choice = ['word_' + str(j) for j in range(1, Constants.total_number + 1)]
                p.participant.vars['list_1'] = zip(indices, anagram_choice, word_choice)

                # Here you can choose to either randomize the same list of anagrams for each participant
                # or select only a random subset of the list (in this case create a variable in Constants which would
                # equal to a number of anagrams to be shown for each participant, e.g. no_select = 10; use this variable
                # instead of Constants.total_number)
                p.participant.vars['pair_select_easy'] = random.sample(Constants.pair_list_easy,
                                                                        Constants.total_number)
                p.participant.vars['pair_select_difficult'] = random.sample(Constants.pair_list_difficult,
                                                                             Constants.total_number)
                p.participant.vars['words_select_easy'] = [x[0] for x in p.participant.vars['pair_select_easy']]
                p.participant.vars['words_select_difficult'] = [x[0] for x in
                                                                p.participant.vars['pair_select_difficult']]
                p.participant.vars['anagram_select_easy'] = [x[1] for x in p.participant.vars['pair_select_easy']]
                p.participant.vars['anagram_select_difficult'] = [x[1] for x in
                                                                  p.participant.vars['pair_select_difficult']]
                p.participant.vars['choices_made'] = []


class Group(BaseGroup):
    pass

class Player(BasePlayer):

    treatment = models.StringField()
    no_anagrams = models.IntegerField()
    correct = models.IntegerField()
    answer = models.StringField()

    for j in range(1, Constants.total_number + 1):
        locals()['anagram_' + str(j)] = models.StringField(blank=True)
    del j
    for j in range(1, Constants.total_number + 1):
        locals()['word_' + str(j)] = models.StringField(blank=True)
    del j

    # Define rule for setting payoff
    def set_payoff(self):
        self.payoff = c(self.correct * Constants.bonus)
        self.participant.vars['correct'] = self.correct
        self.participant.vars['no_anagrams'] = Constants.total_number

    # Define rule for checking correct answers
    def check_correct(self):
        correct = 0
        for j, choice, word in self.participant.vars['list_1']:
            if self.participant.vars['treatment'] == 'easy':
                choice_i = getattr(self, choice)
                self.participant.vars['choices_made'].append(choice_i)
                setattr(self, word, self.participant.vars['words_select_easy'][j - 1])
                if self.participant.vars['choices_made'][j-1] == self.participant.vars['words_select_easy'][j-1]:
                    correct += 1
            else:
                choice_i = getattr(self, choice)
                self.participant.vars['choices_made'].append(choice_i)
                setattr(self, word, self.participant.vars['words_select_difficult'][j - 1])
                if self.participant.vars['choices_made'][j-1] == self.participant.vars['words_select_difficult'][j-1]:
                    correct += 1
        self.correct = correct
        self.set_payoff()

