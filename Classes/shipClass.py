import pygame, GameSpace
pygame.init()


class Ship(pygame.sprite.Sprite):
    #-----------------------------------------------------------------------------------
    """Create a Ship object
    Functions: CreateShip, DrawShip, MoveShip, isWithin
    Attributes: pos, cell_number, cell_size, borders_color, cell_color"""
    #-----------------------------------------------------------------------------------
    def __init__(self, pos, cell_number, cell_size, borders_color, cell_color):
        super().__init__()
        self.pos = pos
        self.x, self.y = pos
        self.cell_number = cell_number
        self.cell_width, self.cell_height = cell_size
        self.cell_group = pygame.sprite.Group()
        self.visible_cells = pygame.sprite.Group()
        self.borders_color = borders_color
        self.cell_color = cell_color
        self.surrounded_cells = pygame.sprite.Group()
        self.collided_cells = pygame.sprite.Group()
        self.put = False
        self.take = False
        self.hor = True
        self.ver = False
        self.alive = True
        self.alive_cells = pygame.sprite.Group()
        self.CreateShip()

    def reinit(self):
        #-----------------------------------------------------------------------------------
        # Reset a ship
        #-----------------------------------------------------------------------------------
        self.x, self.y = self.pos
        self.hor = True
        self.ver = False
        self.put = False
        self.cell_group.empty()
        self.CreateShip()

    def CreateShip(self):
        #-----------------------------------------------------------------------------------
        # Create Ship's cells
        #-----------------------------------------------------------------------------------
        if self.hor:
            self.cell_x, self.cell_y = self.x, self.y
            for cell in range(self.cell_number):
                cell = GameSpace.Cell(self.borders_color, self.cell_color, self.cell_x, self.cell_y, self.cell_width, self.cell_height)
                self.cell_group.add(cell)
                self.alive_cells.add(cell)
                self.cell_x += self.cell_width + 2
            self.rect = pygame.Rect(self.x, self.y, (self.cell_width * self.cell_number) - 26, self.cell_height - 32)
            self.big_rect = pygame.Rect(self.x - self.cell_width - 1, self.y - self.cell_height - 1, (self.cell_width) * (self.cell_number + 2), (self.cell_height) * 3)

        elif self.ver:
            self.cell_x, self.cell_y = self.x, self.y
            for cell in range(self.cell_number):
                cell = GameSpace.Cell(self.borders_color, self.cell_color, self.cell_x, self.cell_y, self.cell_width, self.cell_height)
                self.cell_group.add(cell)
                self.alive_cells.add(cell)
                self.cell_y += self.cell_height + 2
            self.rect = pygame.Rect(self.x, self.y, self.cell_width - 32, (self.cell_height * self.cell_number) - 26)
            self.big_rect = pygame.Rect(self.x - self.cell_width - 1, self.y - self.cell_height - 1, (self.cell_width) * 3, (self.cell_height) * (self.cell_number + 2))

    def DrawShip(self, background):
        #-----------------------------------------------------------------------------------
        # Draw a Ship
        #-----------------------------------------------------------------------------------
        for cell in self.cell_group:
            cell.DrawCell(background)

    def MoveShip(self, mouse_pos):
        #-----------------------------------------------------------------------------------
        # Move ship
        #-----------------------------------------------------------------------------------
        mx, my = mouse_pos
        for value, cell in enumerate(self.cell_group):
            if self.hor:
                if self.isWithin(mouse_pos):
                    self.x, self.y = mx - (value * self.cell_width // 2) - 17, my - 17
                    self.cell_group.empty()
                    self.CreateShip()
            elif self.ver:
                if self.isWithin(mouse_pos):
                    self.x, self.y = mx - 17, my - (value * self.cell_height // 2) - 17
                    self.cell_group.empty()
                    self.CreateShip()

    def isWithin(self, mouse_pos):
        #-----------------------------------------------------------------------------------
        # Check if mouse is within a ship
        #-----------------------------------------------------------------------------------
        mx, my = mouse_pos
        if self.hor:
            if mx > self.x and mx < self.x + self.cell_number * self.cell_width:
                if my > self.y and my < self.y + self.cell_height:
                    return True
            return False

        elif self.ver:
            if mx > self.x and mx < self.x + self.cell_width:
                if my > self.y and my < self.y + self.cell_number * self.cell_height:
                    return True
            return False

    def Hit(self, mouse_pos, player):
        #-----------------------------------------------------------------------------------
        # Hit a Ship
        #-----------------------------------------------------------------------------------
        if self.alive:
            for ship_cell in self.cell_group:
                if ship_cell.isWithin(mouse_pos) and ship_cell in self.alive_cells:
                    self.alive_cells.remove(ship_cell)
                    self.visible_cells.add(ship_cell)
                    player.score += 1

            if len(self.alive_cells.sprites()) == 0:
                self.alive = False
                for ship_cell in self.cell_group:
                    ship_cell.cell_color = (174, 24, 24)
