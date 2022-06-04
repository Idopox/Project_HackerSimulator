import pygame


class Button:
    def __init__(self, x, y, text, text_color, bg_color, font, center_coordinates=False, hover_color=None, size=None,
                 padding=0, outline=0, outline_color=(0, 0, 0)):
        self.x = x
        self.y = y
        self.text = text
        self.text_color = text_color
        self.bg_color = bg_color
        self.font = font
        self.outline = outline
        self.padding = padding
        self.width = self.font.size(self.text)[0] + self.padding * 2
        self.height = self.font.size(self.text)[1] + self.padding * 2
        self.outline_color = outline_color
        self.size = size
        self.hover_color = hover_color
        if center_coordinates:
            if size is None:
                self.x -= self.width / 2
                self.y -= self.height / 2
            else:
                self.x -= size[0] / 2
                self.y -= size[1] / 2

    def draw(self, display, mouse_pos):
        color = self.text_color
        if self.hover_color:
            color = self.hover_color if self.isOver(mouse_pos) else self.text_color
        text = self.font.render(self.text, True, color)

        if self.size is None:
            pygame.draw.rect(display, self.bg_color, (self.x, self.y, self.width, self.height))
            if self.outline > 0:
                pygame.draw.rect(display, self.outline_color, (self.x, self.y, self.width, self.height), self.outline)
            display.blit(text, (self.x + self.padding, self.y + self.padding))
        else:
            pygame.draw.rect(display, self.bg_color, (self.x, self.y, self.size[0], self.size[1]))
            if self.outline > 0:
                pygame.draw.rect(display, self.outline_color, (self.x, self.y, self.size[0], self.size[1]),
                                 self.outline)
            # display text and center it in the button
            display.blit(text, (self.x + (self.size[0] / 2) - (text.get_width() / 2),
                                self.y + (self.size[1] / 2) - (text.get_height() / 2)))

    # Returns true if the given pos (either tuple or list) is over the button
    def isOver(self, pos):
        if self.size is None:
            return self.x < pos[0] < self.x + self.width and pos[1] > self.y and pos[
                1] < self.y + self.height
        else:
            return self.x < pos[0] < self.x + self.size[0] and self.y < pos[1] < self.y + \
                   self.size[1]

    def update_text(self, text):
        self.text = text
        self.width = self.font.size(self.text)[0] + self.padding * 2
        self.height = self.font.size(self.text)[1] + self.padding * 2

class ImageButton:
    def __init__(self, x, y, image, hover_image, size, center_coordinates=False, padding=0, outline=0,
                 outline_color=(0, 0, 0)):
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load(image), size)
        self.hover_image = pygame.transform.scale(pygame.image.load(hover_image), size)
        self.outline = outline
        self.padding = padding
        self.outline_color = outline_color
        self.size = size
        if center_coordinates:
            self.x = x - size[0] / 2
            self.y = y - size[1] / 2
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.hover_rect = self.hover_image.get_rect()
        self.hover_rect.x = self.x
        self.hover_rect.y = self.y
        self.replace = True

    def draw(self, display, mouse_pos):
        if self.replace:
            image, hover_image = self.image, self.hover_image
            rect, hover_rect = self.rect, self.hover_rect
        else:
            image, hover_image = self.hover_image, self.image
            rect, hover_rect = self.hover_rect, self.rect

        if self.hover_image:
            image = hover_image if self.isOver(mouse_pos) else image
            rect = hover_rect if self.isOver(mouse_pos) else rect
        display.blit(image, rect)


    def toggle(self):
        self.replace = not self.replace


    # Returns true if the given pos (either tuple or list) is over the button
    def isOver(self, pos):
        return self.x < pos[0] < self.x + self.size[0] and self.y < pos[1] < self.y + self.size[1]
