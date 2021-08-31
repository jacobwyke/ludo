from piece import Piece
from colour import Colour


class Player:

    colour = None
    
    def __init__(self, colour):
        self.colour = colour
        self.pieces = [Piece(self.colour) for x in range(0, 4)]

    def __str__(self):
        string = str(self.colour)
        return string

    def move(self, number):
        if self.pieces_out():
            self.active_piece().move(number)
        else:
            if number == 6:
                self.next_piece_out().move(number)

    def has_won(self):
        if self.moves_left() == 0:
            return True

        return False

    def pieces_home(self):
        home = 0
        for piece in self.pieces:
            if piece.is_home():
                home += 1

        return home

    def pieces_not_home(self):
        return len(self.pieces) - self.pieces_home()

    def pieces_out(self):
        out = 0
        for piece in self.pieces:
            if piece.is_out():
                out += 1

        return out

    def pieces_in(self):
        x = 0
        for piece in self.pieces:
            if piece.is_in():
                x += 1

        return x

    def active_piece(self):
        for piece in self.pieces:
            if piece.is_out():
                return piece

    def next_piece_out(self):
        for piece in self.pieces:
            if piece.is_in():
                return piece

    def moves_left(self):
        left = 0
        for piece in self.pieces:
            left += piece.moves_left()

        return left
