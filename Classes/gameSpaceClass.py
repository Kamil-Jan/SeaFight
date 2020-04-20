import pygame
class GameSpace(pygame.sprite.Sprite):
    #-----------------------------------------------------------------------------------
    """Create a Game space
    Functions: reinit, CreateGrid, DrawGrid
    Attributes: size, pos, columns, rows, borders_color, cell_size, cell_color"""
    #-----------------------------------------------------------------------------------
    def __init__(self, size, pos, columns, rows, borders_color, cell_size, cell_color):
        super().__init__()
        self.width, self.height = size
        self.x, self.y = pos
        self.cell_x, self.cell_y = pos
        self.columns = columns
        self.rows = rows
        self.borders_color = borders_color
        self.cell_color = cell_color
        self.cell_width, self.cell_height = cell_size
        self.cell_group = pygame.sprite.Group()
        self.chosen_cells = pygame.sprite.Group()

    def reinit(self):
        #-----------------------------------------------------------------------------------
        # Reset a Grid
        #-----------------------------------------------------------------------------------
        for cell in self.cell_group:
            cell.cell_color = (self.cell_color)

    def CreateGrid(self):
        #-----------------------------------------------------------------------------------
        # Create Grid's cells
        #-----------------------------------------------------------------------------------
        self.cell_x, self.cell_y = self.x + 2, self.y + 2
        for row in range(self.rows):
            for column in range(self.columns):
                cell = Cell(self.borders_color, self.cell_color, self.cell_x, self.cell_y, self.cell_width, self.cell_height, column, row)
                self.cell_group.add(cell)
                self.cell_x += self.cell_width + 2
            self.cell_y += self.cell_height + 2
            self.cell_x = self.x + 2

    def DrawGrid(self, background):
        #-----------------------------------------------------------------------------------
        # Draw Grid cells
        #-----------------------------------------------------------------------------------s
        for cell in self.cell_group:
            cell.DrawCell(background)

    def isWithin(self, mouse_pos):
        #-----------------------------------------------------------------------------------
        # Check if mouse if within grid
        #-----------------------------------------------------------------------------------
        mx, my = mouse_pos
        if mx > self.x + 2 and mx < self.x + self.width + 20:
            if my > self.y + 2 and my < self.y + self.height + 20:
                return True

        return False


class Cell(pygame.sprite.Sprite):
    #-----------------------------------------------------------------------------------
    """Create a Cell object
    Functions: DrawCell, isWithin
    Attributes: borders_color, cell_color, cell_x, cell_y, cell_width, cell_height, column=None, row=None"""
    #-----------------------------------------------------------------------------------
    def __init__(self, borders_color, cell_color, cell_x, cell_y, cell_width, cell_height, column=None, row=None):
        super().__init__()
        self.borders_color = borders_color
        self.cell_color = cell_color
        self.cell_x, self.cell_y = cell_x, cell_y
        self.cell_width, self.cell_height = cell_width, cell_height
        self.rect = pygame.Rect(self.cell_x, self.cell_y, self.cell_width, self.cell_height)
        self.column = column
        self.row = row

    def DrawCell(self, background):
        #-----------------------------------------------------------------------------------
        # Draw a Cell
        #-----------------------------------------------------------------------------------
        pygame.draw.rect(background, self.borders_color, (self.cell_x-2, self.cell_y-2, self.cell_width+4, self.cell_height+4))
        pygame.draw.rect(background, self.cell_color, (self.cell_x, self.cell_y, self.cell_width, self.cell_height))

    def isWithin(self, pos):
        #-----------------------------------------------------------------------------------
        # Check if mouse is within a Cell
        #-----------------------------------------------------------------------------------
        if pos[0] > self.cell_x and pos[0] < self.cell_x + self.cell_width:
            if pos[1] > self.cell_y and pos[1] < self.cell_y + self.cell_height:
                return True

        return False
