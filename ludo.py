import sys
import pygame
import random
import time
from board import Board
from colour import Colour
from player import Player


class Ludo:

    number_of_players = 4
    is_playing = True
    players = []
    current_player_id = 0
    current_action = 0
    demo = False

    def __init__(self, demo = False):
        pygame.init()

        self.demo = demo

        self.players = [Player(Colour.COLOURS[x]) for x in range(0, self.number_of_players)]
        self.board = Board(self.players)

        self.play()

    def play(self):
        while self.in_game():

            self.board.current_player(self.current_player())
            self.board.update()

            for event in pygame.event.get():
                if event.type in [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN]:
                    self.next_action()
                elif event.type == pygame.QUIT:
                    self.is_playing = False

            if self.demo:
                time.sleep(0.25)
                self.next_action()

    def next_action(self):
        if self.current_action == 0:
            self.roll()
        elif self.current_action == 1:
            self.wait()
        else:
            self.next_player()

    def roll(self):
        roll = random.randint(1,6)

        self.current_player().move(roll)

        # Knock pieces off the board if we landed on them
        self.knock_off()

        self.board.roll = roll

        self.current_action = 2

    def wait(self):
        self.current_action = 2

    def in_game(self):
        return self.is_playing

    def current_player(self):
        return self.players[self.current_player_id]

    def next_player(self):
        # Roll again if you get a 6
        if self.board.roll != 6:
            self.current_player_id += 1
            if self.current_player_id == self.number_of_players:
                self.current_player_id = 0

        self.board.roll = 0
        self.current_action = 0

    def knock_off(self):
        # Get cell we are on
        if self.current_player().active_piece():
            cell = self.board.get_cell(self.current_player().colour, self.current_player().active_piece().position)

            for player in self.players:
                if player != self.current_player():
                    if player.active_piece():
                        players_cell = self.board.get_cell(player.colour, player.active_piece().position)

                        if cell.track_id == players_cell.track_id:
                            player.active_piece().return_to_start()


if __name__ == "__main__":
    demo = False
    if "-demo" in sys.argv:
        demo = True
    if "-d" in sys.argv:
        demo = True

    if "-h" in sys.argv:
        print("Graphical Ludo Game")
        print("-h\tHelp")
        print("-d/-demo\tRun in demo mode")
    else:
        game = Ludo(demo = demo)
