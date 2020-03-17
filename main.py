import pygame, os
import Appearance, GameSpace, Ship
pygame.init()


class Player():
    #-----------------------------------------------------------------------------------
    """Create player object
    Attributes: Grid
    Functions: CreateShips, DrawShips"""
    #-----------------------------------------------------------------------------------
    def __init__(self, Grid):
        self.ships_group = pygame.sprite.Group()
        self.g_x = Grid.x
        self.score = 0
        self.CreateShips((0, 0, 0), (126, 87, 193))


    def CreateShips(self, borders_color, cell_color):
        """Ship attributes: pos, cell_number, cell_size, borders_color, cell_color"""
        #-----------------------------------------------------------------------------------
        # Create 1 four cell ship
        #-----------------------------------------------------------------------------------
        four_cell_ship = Ship.Ship((self.g_x + 425, 67), 4, (35, 35), borders_color, cell_color)
        self.ships_group.add(four_cell_ship)

        #-----------------------------------------------------------------------------------
        # Create 2 three cell ships
        #-----------------------------------------------------------------------------------
        three_cell_ship_pos = (self.g_x + 425, 115)
        for i in range(2):
            three_cell_ship = Ship.Ship(three_cell_ship_pos, 3, (35, 35), borders_color, cell_color)
            self.ships_group.add(three_cell_ship)
            three_cell_ship_pos = three_cell_ship_pos[0] + 143, three_cell_ship_pos[1]

        #-----------------------------------------------------------------------------------
        # Create 3 two cell ships
        #-----------------------------------------------------------------------------------
        two_cell_ship_pos = (self.g_x + 425, 163)
        for i in range(3):
            two_cell_ship = Ship.Ship(two_cell_ship_pos, 2, (35, 35), borders_color, cell_color)
            self.ships_group.add(two_cell_ship)
            two_cell_ship_pos = two_cell_ship_pos[0] + 90, two_cell_ship_pos[1]

        #-----------------------------------------------------------------------------------
        # Create 4 one cell ships
        #-----------------------------------------------------------------------------------
        one_cell_ship_pos = (self.g_x + 425, 211)
        for i in range(4):
            one_cell_ship = Ship.Ship(one_cell_ship_pos, 1, (35, 35), borders_color, cell_color)
            self.ships_group.add(one_cell_ship)
            one_cell_ship_pos = one_cell_ship_pos[0] + 72, one_cell_ship_pos[1]


    def DrawShips(self, background):
        for ship in self.ships_group:
            ship.DrawShip(background)


def CreateMainMenu():
    #-----------------------------------------------------------------------------------
    """Create Main Menu with buttons
    Menu attributes: size, font, *widgets
    Button attributes: widget_name, text, pos, image_name, color, size"""
    #-----------------------------------------------------------------------------------
    size = background.get_size()
    game_font = pygame.font.SysFont('Arial Black', 25)
    Buttons = [('TwoPlayers', '2 ИГРОКА', (background.get_width() // 2, 125), None, (117, 215, 146), (250, 75)),
               ('Settings', 'НАСТРОЙКИ', (background.get_width() // 2, 225), None, (117, 215, 146), (250, 75))]
    return size, game_font, Buttons


def CheckError(player):
    #-----------------------------------------------------------------------------------
    """Check if all ships are put on the grid"""
    #-----------------------------------------------------------------------------------
    global error
    count = 0
    for ship in player.ships_group:
        if ship.put:
            count += 1

    if count == len(player.ships_group.sprites()):
        error = False
    else:
        error = True

def CreateSurCells(ship, grid):
    #-----------------------------------------------------------------------------------
    """Create Surrounded cells of the ship"""
    #-----------------------------------------------------------------------------------
    ship.surrounded_cells.empty()
    if ship.put:    
        for cell in grid.cell_group:
            if ship.big_rect.colliderect(cell.rect):
                ship.surrounded_cells.add(cell)


def CheckShip(ch_ship, player, grid):
    #-----------------------------------------------------------------------------------
    """Check if a ship is correctly put"""
    #-----------------------------------------------------------------------------------
    # Check if ship collide with other ship's surrounded cells
    for ship in player.ships_group:
        if ship.put:
            for surcell in ship.surrounded_cells:
                if pygame.sprite.collide_rect(ch_ship, surcell):
                    ch_ship.reinit()
                    ch_ship.put = False
                    break
    #-----------------------------------------------------------------------------------
    # Check if a ship outside a grid
    #-----------------------------------------------------------------------------------
    if ch_ship.hor:
        if ch_ship.x + (ch_ship.cell_number * ch_ship.cell_width) > grid.x + grid.width + 22:
            ch_ship.reinit()
            ch_ship.put = False
    elif ch_ship.ver:
        if ch_ship.y + (ch_ship.cell_number * ch_ship.cell_height) > grid.y + grid.height + 22:
            ch_ship.reinit()
            ch_ship.put = False


def ButtonUp(player, Grid):
    #-----------------------------------------------------------------------------------
    """Putting a ship on the grid"""
    #-----------------------------------------------------------------------------------
    # Create ship's collided cells
    #-----------------------------------------------------------------------------------
    for ship in player.ships_group:
        if ship.take:
            #-----------------------------------------------------------------------------------
            # Reset old collided cells of a ship
            #-----------------------------------------------------------------------------------
            ship.collided_cells.empty()
            #-----------------------------------------------------------------------------------
            # Create collided cells
            #----------------------------------------------------------------------------------- 
            for cell in Grid.cell_group:
                if pygame.sprite.collide_rect(ship, cell):
                    ship.collided_cells.add(cell)
            #-----------------------------------------------------------------------------------
            # Update ship's pos
            #-----------------------------------------------------------------------------------
            try:
                ship.x, ship.y = ship.collided_cells.sprites()[0].rect.topleft 
                ship.cell_group.empty()
                ship.alive_cells.empty()
                ship.CreateShip()
                ship.put = True
            except IndexError:
                pass

            CheckShip(ship, player, Grid)
            CheckError(player)
            CreateSurCells(ship, Grid)


def TurnShip(player):
    #-----------------------------------------------------------------------------------
    """Turning a ship"""
    #-----------------------------------------------------------------------------------
    for ship in player.ships_group:
        if ship.take:
            if ship.hor:
                ship.ver = True
                ship.hor = False
                ship.x, ship.y = pos[0] - ship.cell_width // 2, pos[1] - (ship.cell_number * ship.cell_height) // 2
            elif ship.ver:
                ship.hor = True
                ship.ver = False
                ship.x, ship.y = pos[0] - (ship.cell_number * ship.cell_width) // 2, pos[1] - (ship.cell_height) // 2
            ship.cell_group.empty()
            ship.alive_cells.empty()
            ship.CreateShip()


def RedrawScreen():
    #-----------------------------------------------------------------------------------
    """Updating a screen"""
    #-----------------------------------------------------------------------------------
    background.fill((137, 154, 238))
    if showMainMenu:
        #-----------------------------------------------------------------------------------
        # Main Menu update
        #-----------------------------------------------------------------------------------
        MainMenu.DrawWidgets(background, (44, 44, 44))
        background.blit(game_name, (background.get_width() // 2 - game_name.get_width() // 2, 0))

    elif Player1Put:
        #-----------------------------------------------------------------------------------
        # Player1 Grid update
        #-----------------------------------------------------------------------------------
        # Create Menu's environment
        #-----------------------------------------------------------------------------------
        pygame.draw.rect(background, (117, 215, 146), (0, 0, background.get_width(), 50))
        pygame.draw.rect(background, (117, 215, 146), (0, 450, background.get_width(), 50))
        background.blit(player1_name, (background.get_width() // 2 - player1_name.get_width() // 2, 0))

        #-----------------------------------------------------------------------------------
        # Draw Undo and Reset Buttons
        #-----------------------------------------------------------------------------------
        if not error:
            Reset.draw(background, (44, 44, 44))
            try:
                PutMenu.full_widgets_group.draw(background)
            except AttributeError:
                pass

        #-----------------------------------------------------------------------------------
        # Draw all Buttons
        #-----------------------------------------------------------------------------------
        elif error:
            Reset.draw(background, (44, 44, 44))
            try:
                PutMenu.widgets_group.draw(background)
            except AttributeError:
                pass

        for ship in player1.ships_group:
            if ship.put:
                for surcell in ship.surrounded_cells:
                    surcell.cell_color = (170, 170, 170)

        Player1Grid.DrawGrid(background)
        player1.DrawShips(background)

    elif Player2Put:
        #-----------------------------------------------------------------------------------
        # Player2 Grid Update
        #-----------------------------------------------------------------------------------
        # Create Menu's environment
        #-----------------------------------------------------------------------------------
        pygame.draw.rect(background, (117, 215, 146), (0, 0, background.get_width(), 50))
        pygame.draw.rect(background, (117, 215, 146), (0, 450, background.get_width(), 50))
        background.blit(player2_name, (background.get_width() // 2 - player2_name.get_width() // 2, 0))

        #-----------------------------------------------------------------------------------
        # Draw Undo and Reset Buttons
        #-----------------------------------------------------------------------------------
        if not error:
            Reset.draw(background, (44, 44, 44))
            try:
                PutMenu.full_widgets_group.draw(background)
            except AttributeError:
                pass

        #-----------------------------------------------------------------------------------
        # Draw all Buttons
        #-----------------------------------------------------------------------------------
        elif error:
            Reset.draw(background, (44, 44, 44))
            try:
                PutMenu.widgets_group.draw(background)
            except AttributeError:
                pass

        for ship in player2.ships_group:
            if ship.put:
                for surcell in ship.surrounded_cells:
                    surcell.cell_color = (170, 170, 170)

        Player2Grid.DrawGrid(background)
        player2.DrawShips(background)
    
    elif Game:
        #-----------------------------------------------------------------------------------
        # Game Menu updaete
        #-----------------------------------------------------------------------------------
        # Create Game Menu's environment
        #-----------------------------------------------------------------------------------
        pygame.draw.rect(background, (117, 215, 146), (0, 0, background.get_width(), 50))
        pygame.draw.rect(background, (117, 215, 146), (0, 450, background.get_width(), 50))
        background.blit(player1_name, (Player1Grid.x + 372 // 2 - player1_name.get_width() // 2, 0))
        background.blit(player2_name, (Player2Grid.x + 372 // 2 - player2_name.get_width() // 2, 0))
        Player1Grid.DrawGrid(background)
        Player2Grid.DrawGrid(background)

        #-----------------------------------------------------------------------------------
        # Player1 Turn
        #-----------------------------------------------------------------------------------
        if Player1Turn:
            text = player_name_font.render('ХОДИТ ИГРОК 1', 3, (255, 20, 20))
            background.blit(text, (background.get_width() // 2 - text.get_width() // 2, 450))
            Player2Grid.reinit()
            #-----------------------------------------------------------------------------------
            # Paint Player1 Grid
            #-----------------------------------------------------------------------------------
            for cell in Player1Grid.cell_group:
                    cell.cell_color = (200, 200, 200)

        #-----------------------------------------------------------------------------------
        # Player2 Turn
        #-----------------------------------------------------------------------------------
        elif Player2Turn:
            text = player_name_font.render('ХОДИТ ИГРОК 2', 3, (255, 20, 20))
            background.blit(text, (background.get_width() // 2 - text.get_width() // 2, 450))
            Player1Grid.reinit()
            #-----------------------------------------------------------------------------------
            # Paint Player2 Grid
            #-----------------------------------------------------------------------------------
            for cell in Player2Grid.cell_group:
                    cell.cell_color = (200, 200, 200)
        
        #-----------------------------------------------------------------------------------
        # Draw Undo Button
        #-----------------------------------------------------------------------------------
        try:
            PutMenu.widgets_group.draw(background)
        except AttributeError:
            pass

        #-----------------------------------------------------------------------------------
        # Draw Player1 hitten ships' cells
        #-----------------------------------------------------------------------------------
        for ship in player1.ships_group:
            for cell in ship.visible_cells:
                cell.DrawCell(background)
                pygame.draw.line(background, (255, 0, 0), cell.rect.topleft, cell.rect.bottomright, 2)
                pygame.draw.line(background, (255, 0, 0), cell.rect.topright, cell.rect.bottomleft, 2)

        #-----------------------------------------------------------------------------------
        # Draw Player1 missed hits
        #-----------------------------------------------------------------------------------
        for cell in Player1Grid.chosen_cells:
            pygame.draw.circle(background, (0, 0, 0), cell.rect.center, 3, 3)

        #-----------------------------------------------------------------------------------
        # Draw Player2 hiiten ship's cells
        #-----------------------------------------------------------------------------------
        for ship in player2.ships_group:
            for cell in ship.visible_cells:
                cell.DrawCell(background)
                pygame.draw.line(background, (255, 0, 0), cell.rect.topleft, cell.rect.bottomright, 2)
                pygame.draw.line(background, (255, 0, 0), cell.rect.topright, cell.rect.bottomleft, 2)

        #-----------------------------------------------------------------------------------
        # Draw Player2 missed hits
        #-----------------------------------------------------------------------------------
        for cell in Player2Grid.chosen_cells:
            pygame.draw.circle(background, (0, 0, 0), cell.rect.center, 3, 3)

        #-----------------------------------------------------------------------------------
        # Draw End Menu
        #-----------------------------------------------------------------------------------
        if End:
            background.blit(EndMenu_bg, (0, 0))
            EndMenu.DrawWidgets(background, (44, 44, 44))
            if player1.score == 20:
                background.blit(player1_win, (background.get_width() // 2 - player1_win.get_width() // 2, 150))
                background.blit(player2_lose, (background.get_width() // 2 - player2_lose.get_width() // 2, 200))
            else:
                background.blit(player2_win, (background.get_width() // 2 - player2_win.get_width() // 2, 150))
                background.blit(player1_lose, (background.get_width() // 2 - player1_lose.get_width() // 2, 200))

    screen.blit(background, (0, 0))

#-----------------------------------------------------------------------------------
# Initialise Display variables
#-----------------------------------------------------------------------------------
screen = pygame.display.set_mode((832, 500))
pygame.display.set_caption('Морской Бой')
background = pygame.Surface(screen.get_size())
background.fill((137, 154, 238))

#-----------------------------------------------------------------------------------
# Initialise Main Menu
#-----------------------------------------------------------------------------------
size, game_font, Buttons = CreateMainMenu()
game_name_font = pygame.font.SysFont('Arial Black', 60)
game_name = game_name_font.render('МОРСКОЙ БОЙ', 3, (44, 44, 44))
MainMenu = Appearance.Menu(size, game_font, Buttons[0], Buttons[1])
MainMenu.CreateWidgets()

#-----------------------------------------------------------------------------------
# Initialise PutMenu
#-----------------------------------------------------------------------------------
Undo = Appearance.Button('Undo', 'Назад', game_font, (0, 0), 'Arrow1.png', None, None)
Continue = Appearance.Button('Continue', 'Вперед', game_font, (background.get_width() - 30, background.get_height() - 30), 'Arrow.png', None, None)
Reset = Appearance.Button('Reset', 'Сбросить', game_font, (551, 400), None, (255, 215, 146), (150, 35))
PutMenu = Appearance.Menu(size, game_font)
PutMenu.widgets_group.add(Undo, Reset)
PutMenu.full_widgets_group.add(Undo, Continue, Reset)

#-----------------------------------------------------------------------------------
# Initialise EndMenu
#-----------------------------------------------------------------------------------
ToMenu = ('ToMenu', 'В МЕНЮ', (background.get_width() // 2, 325), None, (117, 215, 146), (200, 75))
EndMenu_bg = pygame.Surface(background.get_size())
EndMenu_bg.fill((137, 154, 238))
EndMenu_bg.set_alpha(200)
EndMenu = Appearance.Menu(size, game_font, ToMenu)
EndMenu.CreateWidgets()

#-----------------------------------------------------------------------------------
# Initialise Player1 Grid
#-----------------------------------------------------------------------------------
# GameSpace attributes: size, pos, columns, rows, borders_color, cell_size, cell_color
Player1Grid = GameSpace.GameSpace((350, 350), (76, 65), 10, 10, (0, 0, 0), (35, 35), (255, 255, 255))
Player1Grid.CreateGrid()
player_name_font = pygame.font.SysFont('Arial Black', 30)
player1_name = player_name_font.render('ИГРОК 1', 3, (44, 44, 44))
player1_win = player_name_font.render('ИГРОК 1 - ПОБЕДИТЕЛЬ', 3, (44, 44, 44))
player1_lose = player_name_font.render('ИГРОК 1 - ЛУЗЕР', 3, (44, 44, 44))

#-----------------------------------------------------------------------------------
# Initialise Player2 Grid
#-----------------------------------------------------------------------------------
Player2Grid = GameSpace.GameSpace((350, 350), (76, 65), 10, 10, (0, 0, 0), (35, 35), (255, 255, 255))
Player2Grid.CreateGrid()
player2_name = player_name_font.render('ИГРОК 2', 3, (44, 44, 44))
player2_win = player_name_font.render('ИГРОК 2 - ПОБЕДИТЕЛЬ', 3, (44, 44, 44))
player2_lose = player_name_font.render('ИГРОК 2 - ЛУЗЕР', 3, (44, 44, 44))

#-----------------------------------------------------------------------------------
# Initialise Player object
#-----------------------------------------------------------------------------------
player1 = Player(Player1Grid)
player2 = Player(Player2Grid)

#-----------------------------------------------------------------------------------
# Iinitalise Game varibles
#-----------------------------------------------------------------------------------
clock = pygame.time.Clock()
running = True

showMainMenu = True
Player1Put = True
Player2Put = False
Game = False
GameOn = False
End = False

Player1Turn = True
Player2Turn = False

held = False
error = True

while running:
    clock.tick(60) #120 FPS

    #-----------------------------------------------------------------------------------
    # Main Menu
    #-----------------------------------------------------------------------------------
    if showMainMenu:
        #-----------------------------------------------------------------------------------
        # Reset Player1 environment
        #-----------------------------------------------------------------------------------
        Player1Grid.reinit()
        error = True
        for ship in player1.ships_group:
            ship.reinit()
            ship.surrounded_cells.empty()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            #-----------------------------------------------------------------------------------
            # Quit the game
            #-----------------------------------------------------------------------------------
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            #-----------------------------------------------------------------------------------
            # Mouse if within Menu's widgets
            #-----------------------------------------------------------------------------------
            if event.type == pygame.MOUSEMOTION:
                for widget in MainMenu.widgets_group:
                    #-----------------------------------------------------------------------------------
                    # Change Widget's color
                    #-----------------------------------------------------------------------------------
                    if widget.isWithin(pos):
                        widget.color = (94, 168, 116)
                    else:
                        widget.color = (117, 215, 146)

            if event.type == pygame.MOUSEBUTTONDOWN:
                for widget in MainMenu.widgets_group:
                    #-----------------------------------------------------------------------------------
                    # Click to Two Players Buttons
                    #-----------------------------------------------------------------------------------
                    if widget.isWithin(pos) and widget.name == 'TwoPlayers':
                        Player1Put = True
                        showMainMenu = False

                        Player1Grid.x, Player1Grid.y = (76, 65)
                        Player1Grid.reinit()
                        Player1Grid.cell_group.empty()
                        Player1Grid.CreateGrid()

                        Player2Grid.x, Player2Grid.y = (76, 65)
                        Player2Grid.reinit()
                        Player2Grid.cell_group.empty()
                        Player2Grid.CreateGrid()

    #-----------------------------------------------------------------------------------
    # Player1 Put Menu
    #-----------------------------------------------------------------------------------
    elif Player1Put:
        CheckError(player1)
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            #-----------------------------------------------------------------------------------
            # Quit the game
            #-----------------------------------------------------------------------------------
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            #-----------------------------------------------------------------------------------
            # Mouse if within Menu's widgets
            #-----------------------------------------------------------------------------------
            if event.type == pygame.MOUSEMOTION:
                for widget in PutMenu.full_widgets_group:
                    #-----------------------------------------------------------------------------------
                    # Change Widget's color
                    #-----------------------------------------------------------------------------------
                    if widget.isWithin(pos):
                        widget.color = (94, 168, 116)
                    else:
                        widget.color = (117, 215, 146)

            if event.type == pygame.MOUSEBUTTONDOWN:
                #-----------------------------------------------------------------------------------
                # If all ships are not put on the grid
                #-----------------------------------------------------------------------------------
                if error:
                    for widget in PutMenu.widgets_group:
                        #-----------------------------------------------------------------------------------
                        # Click to Undo Button
                        #-----------------------------------------------------------------------------------
                        if widget.isWithin(pos) and widget.name == 'Undo':
                            #-----------------------------------------------------------------------------------
                            # Back to Main Menu
                            #-----------------------------------------------------------------------------------
                            showMainMenu = True
                            Player1Put = False
                            Player1Grid.reinit()
                            for ship in player1.ships_group:
                                ship.reinit()
                                ship.surrounded_cells.empty()

                        #-----------------------------------------------------------------------------------
                        # Click to Reset Button
                        #-----------------------------------------------------------------------------------
                        if widget.isWithin(pos) and widget.name == 'Reset':
                            #-----------------------------------------------------------------------------------
                            # Reset Player1 environment
                            #-----------------------------------------------------------------------------------
                            error = True
                            Player1Grid.reinit()
                            for ship in player1.ships_group:
                                # Reset ships
                                ship.reinit()
                                ship.surrounded_cells.empty()

                #-----------------------------------------------------------------------------------
                # If all ships are put on the grid
                #-----------------------------------------------------------------------------------
                if not error:
                    for widget in PutMenu.full_widgets_group:
                        #-----------------------------------------------------------------------------------
                        # Click to Undo Button
                        #-----------------------------------------------------------------------------------
                        if widget.isWithin(pos) and widget.name == 'Undo':
                            showMainMenu = True
                            Player1Put = False
                            Player1Grid.reinit()
                            for ship in player1.ships_group:
                                # Reset ships
                                ship.reinit()
                                ship.surrounded_cells.empty()

                        #-----------------------------------------------------------------------------------
                        # Click to Continue Button
                        #-----------------------------------------------------------------------------------
                        if widget.isWithin(pos) and widget.name == 'Continue':
                            Player2Put = True
                            Player1Put = False

                        #-----------------------------------------------------------------------------------
                        # Click to Reset Button
                        #-----------------------------------------------------------------------------------
                        if widget.isWithin(pos) and widget.name == 'Reset':
                            #-----------------------------------------------------------------------------------
                            # Reset Player1 environment
                            #-----------------------------------------------------------------------------------
                            error = True
                            Player1Grid.reinit()
                            for ship in player1.ships_group:
                                ship.reinit()
                                ship.surrounded_cells.empty()

                #-----------------------------------------------------------------------------------
                # Check if player took a ship
                #-----------------------------------------------------------------------------------
                for ship in player1.ships_group:
                    if ship.isWithin(pos):
                        ship.take = True
                        ship.put = False
                    else:
                        ship.take = False
                
                held = True
                pos = pygame.mouse.get_pos()

            #-----------------------------------------------------------------------------------
            # Put a ship
            #-----------------------------------------------------------------------------------
            if event.type == pygame.MOUSEBUTTONUP:
                held = False
                ButtonUp(player1, Player1Grid)

        #-----------------------------------------------------------------------------------
        # Turn a ship 180 deg
        #-----------------------------------------------------------------------------------
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            pygame.time.delay(100) # Except false positives
            TurnShip(player1)

        #-----------------------------------------------------------------------------------
        # Moving a ship if it's taken
        #-----------------------------------------------------------------------------------
        if held:
            for ship in player1.ships_group:
                if ship.take:
                    ship.MoveShip(pos)
                    ship.surrounded_cells.empty()
                    #-----------------------------------------------------------------------------------
                    # Change cells color if they collide with ship
                    #-----------------------------------------------------------------------------------
                    for cell in Player1Grid.cell_group:
                        if pygame.sprite.collide_rect(ship, cell):
                            cell.cell_color = (255, 255, 0)
                        else:
                            cell.cell_color = (255, 255, 255)

    #-----------------------------------------------------------------------------------
    # Player2 Put Menu (Same as Player1 Put Menu)
    #-----------------------------------------------------------------------------------
    elif Player2Put:
        CheckError(player2)
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEMOTION:
                for widget in PutMenu.full_widgets_group:
                    if widget.isWithin(pos):
                        widget.color = (94, 168, 116)
                    else:
                        widget.color = (117, 215, 146)

            if event.type == pygame.MOUSEBUTTONDOWN:
                held = True
                pos = pygame.mouse.get_pos()
                
                if error:
                    for widget in PutMenu.widgets_group:
                        if widget.isWithin(pos) and widget.name == 'Undo':
                            Player1Put = True
                            Player2Put = False
                            Player2Grid.reinit()
                            for ship in player2.ships_group:
                                ship.reinit()
                                ship.surrounded_cells.empty()

                        if widget.isWithin(pos) and widget.name == 'Reset':
                            error = True
                            Player2Grid.reinit()
                            for ship in player2.ships_group:
                                # Reset ships
                                ship.reinit()
                                ship.surrounded_cells.empty()

                if not error:
                    for widget in PutMenu.full_widgets_group:
                        if widget.isWithin(pos) and widget.name == 'Undo':
                            Player1Put = True
                            Player2Put = False
                            Player2Grid.reinit()
                            for ship in player2.ships_group:
                                ship.reinit()
                                ship.surrounded_cells.empty()

                        if widget.isWithin(pos) and widget.name == 'Continue':
                            #-----------------------------------------------------------------------------------
                            # Start a Game
                            #-----------------------------------------------------------------------------------
                            Game = True
                            GameOn = True
                            Player2Put = False
                            count_ship = 0
                            player1.score = 0
                            player2.score = 0

                            #-----------------------------------------------------------------------------------
                            # Create Game environment
                            #-----------------------------------------------------------------------------------
                            Player1Grid.x = 26
                            Player1Grid.reinit()
                            Player1Grid.cell_group.empty()
                            Player1Grid.CreateGrid()
                            for ship in player1.ships_group:
                                ship.cell_group.empty()
                                ship.alive_cells.empty()
                                ship.x -= player1.g_x - Player1Grid.x
                                ship.CreateShip()
                                CreateSurCells(ship, Player1Grid)

                            Player2Grid.x = 429
                            Player2Grid.reinit()
                            Player2Grid.cell_group.empty()
                            Player2Grid.CreateGrid()
                            for ship in player2.ships_group:
                                ship.cell_group.empty()
                                ship.alive_cells.empty()
                                ship.x += Player2Grid.x - player2.g_x
                                ship.CreateShip()
                                CreateSurCells(ship, Player2Grid)

                        if widget.isWithin(pos) and widget.name == 'Reset':
                            error = True
                            Player2Grid.reinit()
                            for ship in player2.ships_group:
                                # Reset ship
                                ship.reinit()
                                ship.surrounded_cells.empty()

                for ship in player2.ships_group:
                    if ship.isWithin(pos):
                        ship.take = True
                        ship.put = False
                    else:
                        ship.take = False

            if event.type == pygame.MOUSEBUTTONUP:
                held = False
                ButtonUp(player2, Player2Grid)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            pygame.time.delay(100)
            TurnShip(player2)

        if held:
            for ship in player2.ships_group:
                if ship.take:
                    ship.MoveShip(pos)
                    ship.surrounded_cells.empty()
                    for cell in Player2Grid.cell_group:
                        if pygame.sprite.collide_rect(ship, cell):
                            cell.cell_color = (255, 255, 0)
                        else:
                            cell.cell_color = (255, 255, 255)

    #-----------------------------------------------------------------------------------
    # Game 
    #-----------------------------------------------------------------------------------
    elif Game and GameOn:
        count_ship = 0
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            #-----------------------------------------------------------------------------------
            # Quit the Game
            #-----------------------------------------------------------------------------------
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                #-----------------------------------------------------------------------------------
                # Click to Undo Button
                #-----------------------------------------------------------------------------------
                if Undo.isWithin(pos):
                    showMainMenu = True
                    Game = False
                    GameOn = False

                #-----------------------------------------------------------------------------------
                # Player1 Hit
                #-----------------------------------------------------------------------------------
                elif Player1Turn:
                    if Player2Grid.isWithin(pos):
                        count_ship = 0
                        for ship in player2.ships_group:
                            if ship.isWithin(pos):
                                ship.Hit(pos, player1)
                                count_ship += 1

                        if count_ship == 0:
                            for cell in Player2Grid.cell_group:
                                if cell.isWithin(pos) and not cell in Player2Grid.chosen_cells:
                                    Player2Grid.chosen_cells.add(cell)
                                    Player2Turn = True
                                    Player1Turn = False

                #-----------------------------------------------------------------------------------
                # Player2 Hit
                #-----------------------------------------------------------------------------------
                elif Player2Turn:
                    if Player1Grid.isWithin(pos):
                        count_ship = 0
                        for ship in player1.ships_group:
                            if ship.isWithin(pos):
                                ship.Hit(pos, player2)
                                count_ship += 1

                        if count_ship == 0:
                            for cell in Player1Grid.cell_group:
                                if cell.isWithin(pos) and not cell in Player1Grid.chosen_cells:
                                    Player1Grid.chosen_cells.add(cell)
                                    Player1Turn = True
                                    Player2Turn = False

        #-----------------------------------------------------------------------------------
        # End of the game
        #-----------------------------------------------------------------------------------
        if player1.score == 20 or player2.score == 20:
            End = True
            GameOn = False

    elif End:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            #-----------------------------------------------------------------------------------
            # Quit the Game
            #-----------------------------------------------------------------------------------
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEMOTION:
                for widget in EndMenu.widgets_group:
                    if widget.isWithin(pos):
                        widget.color = (94, 168, 116)
                    else:
                        widget.color = (117, 215, 146)

            if event.type == pygame.MOUSEBUTTONDOWN:
                for widget in EndMenu.widgets_group:
                    if widget.isWithin(pos) and widget.name == 'ToMenu':
                        showMainMenu = True
                        End = False
                        Game = False

    RedrawScreen()
    pygame.display.update()
