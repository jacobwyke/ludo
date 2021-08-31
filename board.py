import pygame
import csv
from cell import Cell


class Board:

    # Size of each block in px
    cell_size = 50

    # Size of the grid used in Ludo
    grid_size = 15

    border_size = 3

    player = None

    roll = 0

    track = {}

    line_color = pygame.Color("black")
    track_color = pygame.Color("white")

    def __init__(self, players):
        self.screen_width = (self.cell_size * self.grid_size) + ((self.grid_size - 1) * self.border_size)
        self.screen_height = (self.cell_size * self.grid_size) + ((self.grid_size - 1) * self.border_size)

        self.players = players

        self.show_window()
        self.update()

    def get_grid(self):
        grid = [list([] for x in range(0, self.grid_size)) for y in range(0, self.grid_size)]

        colours = list(csv.reader(open("data/colour.csv")))
        track = list(csv.reader(open("data/track.csv")))

        for y in range(0, self.grid_size):
            for x in range(0, self.grid_size):
                grid[x][y] = Cell(x, y, colours[y][x], track[y][x])
                grid[x][y].draw(self.screen)

                if track[y][x] != "-":
                    self.track[track[y][x]] = grid[x][y]

        return grid

    def show_window(self):
        # Set window title bar
        pygame.display.set_caption("Ludo")

        # Set the size of the window
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

    def current_player(self, player):
        self.player = player

    def show_whos_turn(self):
        if not self.roll:
            font = pygame.font.Font('freesansbold.ttf', 35)
            text = font.render(str(self.player), True, pygame.Color("black"))
            textRect = text.get_rect()
            textRect.center = (self.screen_width // 2, self.screen_height // 2)
            self.screen.blit(text, textRect)

    def show_roll(self):
        if self.roll:
            font = pygame.font.Font('freesansbold.ttf', 90)
            text = font.render(str(self.roll), True, pygame.Color("black"))
            textRect = text.get_rect()
            textRect.center = (self.screen_width // 2, self.screen_height // 2)
            self.screen.blit(text, textRect)

    def show_pieces(self):
        for player in self.players:
            for piece in player.pieces:
                if piece.is_out():
                    self.get_cell(player.colour, piece.position).draw_piece(self.screen, player.colour)

    def show_bases(self):
        for player in self.players:
            self.show_base(player)

    def show_base(self, player):
        # Get the base position for each colour
        if player.colour == "RED":
            base_position = self.grid[0][0].position()
            inner_position = self.grid[1][1].position()
            colour = pygame.Color("red")
        elif player.colour == "GREEN":
            base_position = self.grid[9][0].position()
            inner_position = self.grid[10][1].position()
            colour = pygame.Color("green")
        elif player.colour == "YELLOW":
            base_position = self.grid[9][9].position()
            inner_position = self.grid[10][10].position()
            colour = pygame.Color("gold")
        elif player.colour == "BLUE":
            base_position = self.grid[0][9].position()
            inner_position = self.grid[1][10].position()
            colour = pygame.Color("skyblue")

        # Work out the size
        base_size = (self.cell_size + self.border_size) * 6 - self.border_size
        inner_size = (self.cell_size + self.border_size) * 4 - self.border_size

        pygame.draw.rect(self.screen, colour, pygame.Rect(base_position, (base_size, base_size)))

        pygame.draw.rect(self.screen, pygame.Color("black"), pygame.Rect((inner_position[0] - self.border_size, inner_position[1] - self.border_size), (inner_size + (self.border_size * 2), inner_size + (self.border_size * 2))))
        pygame.draw.rect(self.screen, pygame.Color("white"), pygame.Rect(inner_position, (inner_size, inner_size)))

        for x in range(0, player.pieces_in()):
            size = self.cell_size/1.5
            if x == 0:
                piece_position = (inner_position[0] + (self.cell_size), inner_position[1] + (self.cell_size))
            elif x == 1:
                piece_position = (inner_position[0] + (self.cell_size * 3), inner_position[1] + (self.cell_size))
            elif x == 2:
                piece_position = (inner_position[0] + (self.cell_size), inner_position[1] + (self.cell_size * 3))
            elif x == 3:
                piece_position = (inner_position[0] + (self.cell_size * 3), inner_position[1] + (self.cell_size * 3))

            pygame.draw.circle(self.screen, colour, piece_position, size)
            pygame.draw.circle(self.screen, pygame.Color("black"), piece_position, size, 2)


    def show_extra_graphics(self):
        # Home arrows
        top_left = ((self.cell_size + self.border_size) * 6, (self.cell_size + self.border_size) * 6)
        top_right = ((self.cell_size + self.border_size) * 9 - self.border_size - 1, (self.cell_size + self.border_size) * 6)
        bottom_left = ((self.cell_size + self.border_size) * 6, (self.cell_size + self.border_size) * 9 - self.border_size - 1)
        bottom_right = ((self.cell_size + self.border_size) * 9 - self.border_size, (self.cell_size + self.border_size) * 9 - self.border_size - 1)
        middle = (self.screen_width / 2, self.screen_height / 2)

        pygame.draw.polygon(self.screen, pygame.Color("red"), [top_left, bottom_left, middle])
        pygame.draw.polygon(self.screen, pygame.Color("green"), [top_left, top_right, middle])
        pygame.draw.polygon(self.screen, pygame.Color("gold"), [top_right, bottom_right, middle])
        pygame.draw.polygon(self.screen, pygame.Color("skyblue"), [bottom_left, bottom_right, middle])

        # Start arrows
        red_out_top_left = (self.cell_size + self.border_size, (self.cell_size + self.border_size) * 6)
        red_out_top_right = (red_out_top_left[0] + self.cell_size - 1, red_out_top_left[1])
        red_out_middle =  (red_out_top_left[0] + (self.cell_size / 2), red_out_top_left[1] + (self.cell_size / 2))

        green_out_top_right = ((self.cell_size + self.border_size) * 9 - self.border_size - 1, (self.cell_size + self.border_size) * 1)
        green_out_bottom_right = (green_out_top_right[0], green_out_top_right[1] + self.cell_size - 1)
        green_out_middle =  (green_out_top_right[0] - (self.cell_size / 2), green_out_top_right[1] + (self.cell_size / 2))

        yellow_out_bottom_left = ((self.cell_size + self.border_size) * 13, (self.cell_size + self.border_size) * 9 - self.border_size - 1)
        yellow_out_bottom_right = (yellow_out_bottom_left[0]+ self.cell_size - 1, yellow_out_bottom_left[1])
        yellow_out_middle =  (yellow_out_bottom_left[0] + (self.cell_size / 2), yellow_out_bottom_left[1] - (self.cell_size / 2))

        blue_out_top_left = ((self.cell_size + self.border_size) * 6, (self.cell_size + self.border_size) * 13)
        blue_out_bottom_left = (blue_out_top_left[0], blue_out_top_left[1] + self.cell_size - 1)
        blue_out_middle =  (blue_out_top_left[0] + (self.cell_size / 2), blue_out_top_left[1] + (self.cell_size / 2))

        pygame.draw.polygon(self.screen, pygame.Color("red"), [red_out_top_left, red_out_top_right, red_out_middle])
        pygame.draw.polygon(self.screen, pygame.Color("green"), [green_out_top_right, green_out_bottom_right, green_out_middle])
        pygame.draw.polygon(self.screen, pygame.Color("gold"), [yellow_out_bottom_left, yellow_out_bottom_right, yellow_out_middle])
        pygame.draw.polygon(self.screen, pygame.Color("skyblue"), [blue_out_top_left, blue_out_bottom_left, blue_out_middle])


        # Try and show the pieces home
        # for player in self.players:
        #     for x in range(0, player.pieces_home()):
        #         size = self.cell_size / 2
        #         if x == 0:
        #             piece_position = (inner_position[0] + (self.cell_size), inner_position[1] + (self.cell_size))
        #         elif x == 1:
        #             piece_position = (inner_position[0] + (self.cell_size * 3), inner_position[1] + (self.cell_size))
        #         elif x == 2:
        #             piece_position = (inner_position[0] + (self.cell_size), inner_position[1] + (self.cell_size * 3))
        #         elif x == 3:
        #             piece_position = (inner_position[0] + (self.cell_size * 3), inner_position[1] + (self.cell_size * 3))

    def get_cell(self, colour, position):
        offset = {
            "RED": 0,
            "GREEN": 13,
            "YELLOW": 26,
            "BLUE": 39
        }

        # Onto the home row
        if position > 51:
            if colour == "RED":
                position = "1-"+str(position)
            elif colour == "YELLOW":
                position = "2-"+str(position)
            elif colour == "GREEN":
                position = "3-"+str(position)
            elif colour == "BLUE":
                position = "4-"+str(position)
        else:
            position += offset[colour]
            if position > 51:
                # to account for the first grid being 0
                position -= 52

        return self.track[str(position)]

    def update(self):
        self.draw_board()
        pygame.display.flip()

    def draw_board(self):
        # Fill screen with black
        self.screen.fill(self.line_color)

        self.grid = self.get_grid()

        self.show_bases()
        self.show_extra_graphics()

        self.show_pieces()

        self.show_whos_turn()
        self.show_roll()
