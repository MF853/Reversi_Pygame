import pygame
from utils.constants import *

class Button:
    def __init__(self, position, size, color=(0, 0, 0, 0)):
        self.status = BTN_STATUS.ACTIVE
        self.color = color
        self.position = position
        self.size = size
        self.rect = pygame.Rect(self.position, self.size)

    def draw(self, surface):
        # Create a transparent surface with the same size as the button rect
        transparent_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        transparent_surface.fill(self.color)

        # Blit the transparent surface onto the button rect
        surface.blit(transparent_surface, self.rect.topleft)

    def is_pressed(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
    def update_status(self, mouse_pos, disabled = False):
        if disabled:
            self.status = BTN_STATUS.DISABLED
            
        else:
            if self.rect.collidepoint(mouse_pos):
                self.status = BTN_STATUS.HOVERED
            else:
                self.status = BTN_STATUS.ACTIVE

        self.color = self.status

class CircleButton:
    def __init__(self, position, size, color=(0, 0, 0, 0)):
        self.status = BTN_STATUS.ACTIVE
        self.color = color
        self.position = position
        self.size = size
        self.rect = pygame.Rect(self.position, self.size)

    def draw(self, surface):
        # Create a transparent surface with the same size as the button rect
        transparent_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        transparent_surface.fill((0, 0, 0, 0))

        # Draw a circle inside the transparent surface
        circle_radius = min(self.rect.width, self.rect.height) // 2
        circle_center = (self.rect.width // 2, self.rect.height // 2)
        pygame.draw.circle(transparent_surface, self.color, circle_center, circle_radius)

        # Blit the transparent surface onto the button rect
        surface.blit(transparent_surface, self.rect.topleft)

    def is_pressed(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
    def update_status(self, mouse_pos, disabled = False):
        if disabled:
            self.status = BTN_STATUS.DISABLED
            
        else:
            if self.rect.collidepoint(mouse_pos):
                self.status = BTN_STATUS.HOVERED
            else:
                self.status = BTN_STATUS.ACTIVE

        self.color = self.status
    
def set_rounded(color, roundness, surface):
        size = surface.get_size()
        r, c = roundness, color
        pygame.draw.rect(surface, c, (r, 0, size[0]-2*r, size[1]))
        pygame.draw.rect(surface, c, (0, r, size[0], size[1]-2*r))
        for cpt in [(r, r), (size[0]-r, r), (r, size[1]-r), (size[0]-r, size[1]-r)]:  
            pygame.draw.circle(surface, c, cpt, r)

class RoundedRectBorderButton:
    def __init__(self, position, size, color=(0, 0, 0, 0)):
        self.status = BTN_STATUS.ACTIVE
        self.color = color
        self.position = position
        self.size = size
        self.rect = pygame.Rect(self.position, self.size)

    def draw(self, surface):
        # Create a transparent surface with the same size as the button rect
        transparent_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        transparent_surface.fill((0, 0, 0, 0))

        # Draw the rounded rectangle border on the transparent surface
        set_rounded(self.color, min(self.rect.width, self.rect.height) // 2, transparent_surface)

        # Draw a border around the
        # pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)

        # Blit the transparent surface onto the button rect
        surface.blit(transparent_surface, self.rect.topleft)

    def is_pressed(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
    def update_status(self, mouse_pos, disabled):
        if disabled:
            self.status = BTN_STATUS.DISABLED

        else:
            if self.rect.collidepoint(mouse_pos):
                self.status = BTN_STATUS.HOVERED
            else:
                self.status = BTN_STATUS.ACTIVE

        self.color = self.status
    
class TextBox:
    def __init__(self, position, size, text, font, text_color, color=(0, 0, 0, 0)):
        self.color = color
        self.position = position
        self.size = size
        self.rect = pygame.Rect(position, size)
        self.text = text
        self.font = font
        self.text_color = text_color

    def draw1(self, surface):
        # Create a transparent surface with the same size as the rectangle
        transparent_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        transparent_surface.fill((0, 0, 0, 0))

        # Draw the rectangle on the transparent surface
        pygame.draw.rect(transparent_surface, self.color, transparent_surface.get_rect())

        # Render the text
        text_surface = self.font.render(self.text, True, self.text_color)

        # Calculate the scaling factor based on the larger dimension of the TextBox
        scaling_factor = min(self.size[0] / text_surface.get_width(), self.size[1] / text_surface.get_height())

        # Scale the text surface while maintaining aspect ratio
        scaled_size = (int(text_surface.get_width() * scaling_factor), int(text_surface.get_height() * scaling_factor))
        text_surface = pygame.transform.smoothscale(text_surface, scaled_size)

        # Blit the text onto the transparent surface
        text_rect = text_surface.get_rect(center=transparent_surface.get_rect().center)
        transparent_surface.blit(text_surface, text_rect)

        # Blit the transparent surface onto the main surface
        surface.blit(transparent_surface, self.position)

    def draw(self, surface):
        # Render each line of text separately and calculate the total height
        lines = self.text.split('\n')
        total_height = 0
        text_surfaces = []

        # The size will be based on the largest string
        largest_str = max(lines, key=len)

        # Render the line of text
        text_surface = self.font.render(largest_str.strip(), True, self.text_color)

        # Check if text_surface has non-zero width and height
        if text_surface.get_width() == 0 or text_surface.get_height() == 0:
            # Handle the case of empty text or font rendering issue
            return

        # Calculate the scaling factor based on the width
        fs = .8
        scaling_factor = min(self.size[0] / text_surface.get_width(), self.size[1] / text_surface.get_height()) * fs

        for line in lines:
            # Render the line of text
            text_surface = self.font.render(line.strip(), True, self.text_color)

            # Scale the text surface while maintaining aspect ratio
            scaled_size = (int(text_surface.get_width() * scaling_factor), int(text_surface.get_height() * scaling_factor))
            scaled_text_surface = pygame.transform.smoothscale(text_surface, scaled_size)

            # Update the total height
            total_height += scaled_text_surface.get_height()

            text_surfaces.append(scaled_text_surface)

        # Create a transparent surface
        total_size = (int(self.size[0]), int(total_height))
        transparent_total_surface = pygame.Surface(total_size, pygame.SRCALPHA)
        transparent_total_surface.fill((0, 0, 0, 0))

        # Draw the rectangle on the transparent surface
        pygame.draw.rect(transparent_total_surface, self.color, transparent_total_surface.get_rect())

        
        for i, text_surface in enumerate(text_surfaces):
            # Blit the scaled text onto the transparent surface
            text_rect = text_surface.get_rect(center=transparent_total_surface.get_rect().center)
            h_f = sum([txt_surf.get_height() for txt_surf in text_surfaces[0:i]]) if i != 0 else 0
            text_rect.top = (transparent_total_surface.get_height() - total_height)*.5 + h_f
            transparent_total_surface.blit(text_surface, text_rect)
            
        surface.blit(transparent_total_surface, self.position)


class Peg:
    def __init__(self, top_left_position, row, col, size, color=(0, 0, 0, 0)):
        self.color = color
        self.status = BTN_STATUS.ACTIVE
        self.top_left_position = top_left_position
        self.size = size
        self.rect = pygame.Rect(
            col * self.size[0] + self.top_left_position[0], 
            row * self.size[1] + self.top_left_position[1], 
            self.size[0], 
            self.size[1]
        )

        # Load player images and resize them
        self.player1_image = pygame.image.load("./assets/players/pedrapreta.png").convert_alpha()
        self.player2_image = pygame.image.load("./assets/players/pedrabranca.png").convert_alpha()

        # Resize images to match the size of the circles
        circle_radius = min(self.size[0], self.size[1]) // 2
        self.player1_image = pygame.transform.smoothscale(self.player1_image, (circle_radius * 2, circle_radius * 2))
        self.player2_image = pygame.transform.smoothscale(self.player2_image, (circle_radius * 2, circle_radius * 2))

    def draw(self, surface, position, expected_child, is_valid, current_player):
        row, col = position[0], position[1]

        # Create a transparent surface with the same size as the rect
        transparent_surface = pygame.Surface(self.size, pygame.SRCALPHA)
        transparent_surface.fill((0, 0, 0, 0))

        # Draw a border around the
        # pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)

        cell_color = PEG_COLORS[expected_child] if expected_child != EMPTY else (*PEG_COLORS[current_player][:3], 80)
            
        if expected_child == X:
            # Draw the resized player 1 image
            surface.blit(self.player1_image, self.rect.topleft)
        
        elif expected_child == O:
            # Draw the resized player 2 image
            surface.blit(self.player2_image, self.rect.topleft)

        else:
            if is_valid(row, col, current_player):
                # Draw a circle inside the transparent surface
                circle_radius = min(self.rect.width, self.rect.height) // 2
                circle_center = (self.rect.width // 2, self.rect.height // 2)
                padding = 5
                pygame.draw.circle(transparent_surface, cell_color, circle_center, circle_radius - padding)
                padding *= 2
                pygame.draw.circle(transparent_surface, (0, 0, 0, 0), circle_center, circle_radius - padding)

                # Blit the transparent surface onto the button rect
                surface.blit(transparent_surface, self.rect.topleft)

    def is_pressed(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
    def update_status(self, mouse_pos, disabled):
        if disabled:
            self.status = BTN_STATUS.DISABLED

        else:
            if self.rect.collidepoint(mouse_pos):
                self.status = BTN_STATUS.HOVERED
            else:
                self.status = BTN_STATUS.ACTIVE

        self.color = self.status

class Overlay:
    def __init__(self, position, size, color=(0, 0, 0, 0)):
        self.color = color
        self.position = position
        self.size = size
        self.rect = pygame.Rect(self.position, self.size)

    def draw(self, surface):
        # Create a transparent surface with the same size as the button rect
        transparent_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        transparent_surface.fill((0, 0, 0, 0))

        # Draw the rounded rectangle border on the transparent surface
        set_rounded(self.color, int(min(self.size[0], self.size[1]) * 0.04), transparent_surface)

        # Blit the transparent surface onto the button rect
        surface.blit(transparent_surface, self.rect.topleft)