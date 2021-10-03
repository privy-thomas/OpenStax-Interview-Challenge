#!/usr/bin/env python3
from random import randrange


class Game:
    def __init__(self, no_of_players):
        self.players = []
        self.places = [0] * no_of_players
        self.purses = [0] * no_of_players
        self.in_penalty_box = [0] * no_of_players

        self.pop_questions = []
        self.science_questions = []
        self.sports_questions = []
        self.rock_questions = []

        self.current_player = 0
        self.is_getting_out_of_penalty_box = False

        self.WIN_CONDITION = 6

        for i in range(50):
            self.create_pop_questions("Pop Question %s" % i)
            self.create_science_questions("Science Question %s" % i)
            self.create_sports_questions("Sports Question %s" % i)
            self.create_rock_question("Rock Question %s" % i)

    def create_pop_questions(self, question):
        self.pop_questions.append(question)

    def create_science_questions(self, question):
        self.science_questions.append(question)

    def create_sports_questions(self, question):
        self.sports_questions.append(question)

    def create_rock_question(self, question):
        self.rock_questions.append(question)

    def is_playable(self):
        return self.how_many_players >= 2

    def add(self, player_name):
        self.players.append(player_name)
        self.places[self.how_many_players - 1] = 0
        self.purses[self.how_many_players - 1] = 0
        self.in_penalty_box[self.how_many_players - 1] = False

        print(player_name + " was added")
        print("They are player number %s" % len(self.players))

        return True

    @property
    def how_many_players(self):
        return len(self.players)

    def roll(self, roll):
        if not(self.is_playable()):
            print("Need to least 2 active players")
            exit(0)

        print("%s is the current player" % self.players[self.current_player])
        print("They have rolled a %s" % roll)

        if self.in_penalty_box[self.current_player]:
            if roll % 2 != 0:
                self.is_getting_out_of_penalty_box = True

                print("%s is getting out of the penalty box" % self.players[self.current_player])
                self.places[self.current_player] = self.places[self.current_player] + roll
                if self.places[self.current_player] > 11:
                    self.places[self.current_player] = self.places[self.current_player] - 12

                print(self.players[self.current_player] + \
                            '\'s new location is ' + \
                            str(self.places[self.current_player]))
                print("The category is %s" % self._current_category)
                self._ask_question()
            else:
                print("%s is not getting out of the penalty box" % self.players[self.current_player])
                self.is_getting_out_of_penalty_box = False
        else:
            self.places[self.current_player] = self.places[self.current_player] + roll
            if self.places[self.current_player] > 11:
                self.places[self.current_player] = self.places[self.current_player] - 12

            print(self.players[self.current_player] + \
                        '\'s new location is ' + \
                        str(self.places[self.current_player]))
            print("The category is %s" % self._current_category)
            self._ask_question()

    def _ask_question(self):
        if self._current_category == 'Pop':
            question = self.pop_questions.pop(0)
            print(question)
            self.pop_questions.append(question)
        elif self._current_category == 'Science':
            question = self.science_questions.pop(0)
            print(question)
            self.science_questions.append(question)
        elif self._current_category == 'Sports':
            question = self.sports_questions.pop(0)
            print(question)
            self.sports_questions.append(question)
        elif self._current_category == 'Rock':
            question = self.rock_questions.pop(0)
            print(question)
            self.rock_questions.append(question)

    @property
    def _current_category(self):
        if self.places[self.current_player] % 4 == 0:
            return 'Pop'
        elif self.places[self.current_player] % 4 == 1:
            return 'Science'
        elif self.places[self.current_player] % 4 == 2:
            return 'Sports'
        return 'Rock'

    def was_correctly_answered(self):
        if self.in_penalty_box[self.current_player]:
            if self.is_getting_out_of_penalty_box:
                print('Answer was correct!!!!')
                self.purses[self.current_player] += 1
                print(self.players[self.current_player] + \
                    ' now has ' + \
                    str(self.purses[self.current_player]) + \
                    ' Gold Coins.')

                winner = self._did_player_win()
                self.current_player += 1
                if self.current_player == len(self.players):
                    self.current_player = 0

                return winner
            else:
                self.current_player += 1
                if self.current_player == len(self.players):
                    self.current_player = 0
                return True



        else:

            print("Answer was corrent!!!!")
            self.purses[self.current_player] += 1
            print(self.players[self.current_player] + \
                ' now has ' + \
                str(self.purses[self.current_player]) + \
                ' Gold Coins.')

            winner = self._did_player_win()
            self.current_player += 1
            if self.current_player == len(self.players):
                self.current_player = 0

            return winner

    def wrong_answer(self):
        print('Question was incorrectly answered')
        print(self.players[self.current_player] + " was sent to the penalty box")
        self.in_penalty_box[self.current_player] = True

        self.current_player += 1
        if self.current_player == len(self.players):
            self.current_player = 0
        return True

    def _did_player_win(self):
        return not (self.purses[self.current_player] == self.WIN_CONDITION)

    def answer_question(self, answer):
        if answer == 0:  # check if answer was correct
            return self.was_correctly_answered()
        else:
            return self.wrong_answer()


if __name__ == '__main__':
    not_a_winner = True

    game = Game(10)

    for i in range(10):
        game.add("Player " + str(i))

    while not_a_winner:
        game.roll(randrange(5) + 1)
        ans = randrange(2)
        not_a_winner = game.answer_question(ans)

    print("\n\n", game.pop_questions)
    print(game.rock_questions)
    print(game.science_questions)
    print(game.sports_questions)
