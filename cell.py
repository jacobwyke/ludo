import pygame


class Cell:

    def __init__(self, x, y, colour_id, track_id = None, cell_size = 50, border_size = 3):
        self.x = x
        self.y = y
        self.colour_id = int(colour_id)
        self.track_id = track_id
        self.cell_size = cell_size
        self.border_size = border_size

    def __str__(self):
        return str(self.x) + " / " + str(self.y) + " / " + str(self.colour()) + " / " + str(self.track_id)

    def colour(self):
        if self.colour_id == 0:
            return pygame.Color("white")
        elif self.colour_id == 1:
            return pygame.Color("red")
        elif self.colour_id == 2:
            return pygame.Color("green")
        elif self.colour_id == 3:
            return pygame.Color("skyblue")
        elif self.colour_id == 4:
            return pygame.Color("gold")
        else:
            return pygame.Color("black")

    def position(self, offset = 0):
        x = (self.x * (self.cell_size + self.border_size)) + offset
        y = (self.y * (self.cell_size + self.border_size)) + offset

        return (x, y)

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour(), pygame.Rect(self.position(), (self.cell_size, self.cell_size)))

    def draw_piece(self, screen, colour):
        if colour == "RED":
            colour = pygame.Color("red")
        elif colour == "GREEN":
            colour = pygame.Color("green")
        elif colour == "YELLOW":
            colour = pygame.Color("gold")
        elif colour == "BLUE":
            colour = pygame.Color("skyblue")

        pygame.draw.circle(screen, colour, self.position(self.cell_size / 2), 20)
        pygame.draw.circle(screen, pygame.Color("black"), self.position(self.cell_size / 2), 20, 2)
