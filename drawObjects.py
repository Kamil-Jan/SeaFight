import pygame


def RedrawScreen():
    #-----------------------------------------------------------------------------------
    """Updating a screen"""
    #-----------------------------------------------------------------------------------
    background.fill((137, 154, 238))
    if showMainMenu:
        #-----------------------------------------------------------------------------------
        # Main Menu update
        #-----------------------------------------------------------------------------------
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
        # Draw Back and Reset Buttons
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
        # Draw Back and Reset Buttons
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
            text = player_name_font.render('TURN - PLAYER 1', 3, (255, 20, 20))
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
            text = player_name_font.render('TURN - PLAYER 2', 3, (255, 20, 20))
            background.blit(text, (background.get_width() // 2 - text.get_width() // 2, 450))
            Player1Grid.reinit()
            #-----------------------------------------------------------------------------------
            # Paint Player2 Grid
            #-----------------------------------------------------------------------------------
            for cell in Player2Grid.cell_group:
                    cell.cell_color = (200, 200, 200)

        #-----------------------------------------------------------------------------------
        # Draw Back Button
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
