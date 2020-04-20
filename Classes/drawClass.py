def drawClass:
    """Class with draw functions.

    Functions:
         drawLobby();
         drawPlayerPut(player, error);
         drawGame(aPlayer, pPlayer, aPlayerGrid, pPlayerGrid)

    Attributes: bg, lobbyMenu, putMenu, endMenu"""
    def __init__(self, bg, lobbyMenu, putMenu, endMenu):
        self.bg = bg
        self.lobbyMenu = lobbyMenu
        self.putMenu = putMenu
        self.endMenu = endMenu

    def drawLobby(self):
        """Draw Main Menu."""
        # Draw main Menu's buttons.
        self.lobbyMenu.DrawWidgets(self.bg, (44, 44, 44))
        # Draw game name label.
        gameName = self.lobbyMenu.gameName
        gN_pos = (self.bg.get_width()//2 - gameName.get_width()//2, 0)
        self.bg.blit(game_name, gN_pos)

    # TODO: drawPlayerPut
    # TODO: drawGame
