import pygame
import os
pygame.init()


class Menu():
    #-----------------------------------------------------------------------------------
    """Create a menu space
    Functions: CreateWidgets, DrawWidgets
    Attributes: widget_name, text, pos, image_name, color, size"""
    #-----------------------------------------------------------------------------------
    def __init__(self, size, font, *widgets):
        self.width, self.height = size
        self.font = font
        self.widgets = list(widgets)
        self.widgets_group = pygame.sprite.Group()
        self.full_widgets_group = pygame.sprite.Group()

    def CreateWidgets(self):
        #-----------------------------------------------------------------------------------
        # Create Menu's widgets
        #-----------------------------------------------------------------------------------
        for widget, text, pos, image_name, color, size in self.widgets:
            widget = Button(widget, text, self.font, pos, image_name, color, size)
            self.widgets_group.add(widget)

    def DrawWidgets(self, background, outline):
        #-----------------------------------------------------------------------------------
        # Draw Widget with outline
        #-----------------------------------------------------------------------------------
        for widget in self.widgets_group:
            widget.draw(background, outline)


class Button(pygame.sprite.Sprite):
    #-----------------------------------------------------------------------------------
    """Create a Button
    Functions: draw, isWithin
    Attributes: image_name, text, font, color, pos, size"""
    #-----------------------------------------------------------------------------------
    def __init__(self, name, text, font, pos, image_name=None, color=None, size=None):
        super().__init__()
        self.name = name
        self.text = text
        self.font = font
        if image_name is not None:
            self.image, self.rect = load_png(image_name)
            self.width, self.height = self.image.get_size()
            self.x, self.y = pos[0], pos[1]
            self.rect.move_ip(self.x, self.y)
        else:
            self.color = color
            self.width, self.height = size
            self.x, self.y = pos[0] - self.width // 2, pos[1]
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        

    def draw(self, background, outline=None):
        #-----------------------------------------------------------------------------------
        # Draw outlined rectangle
        #-----------------------------------------------------------------------------------
        pygame.draw.rect(background, outline, (self.x-2, self.y-2, self.width+4, self.height+4))
        pygame.draw.rect(background, self.color, (self.x, self.y, self.width, self.height))

        #-----------------------------------------------------------------------------------
        # Draw space in the middle of the rectangle
        #-----------------------------------------------------------------------------------
        text = self.font.render(self.text, 1, outline)
        background.blit(text, (self.x + (self.width // 2 - text.get_width() // 2), self.y + (self.height // 2 - text.get_height() // 2)))

    def isWithin(self, pos):
        #-----------------------------------------------------------------------------------
        # Check if mouse if within Button
        #-----------------------------------------------------------------------------------
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


def load_png(name):
    #-----------------------------------------------------------------------------------
    """ Load image and return image object"""
    #-----------------------------------------------------------------------------------
    path = os.path.join(os.path.dirname(__file__), 'data', name)
    image = pygame.image.load(path)

    if image.get_alpha() is None:
        image = image.convert()
    else:
        image = image.convert_alpha()

    return image, image.get_rect()
