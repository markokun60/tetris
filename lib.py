import pygame
import math

def render_text_effects(surface, text, font, time_elapsed,width,height):
    """Render text with color, fade, and scale effects."""
    # Color cycling effect (RGB sine wave)
    r = int(128 + 127 * math.sin(time_elapsed * 2))
    g = int(128 + 127 * math.sin(time_elapsed * 2 + 2))
    b = int(128 + 127 * math.sin(time_elapsed * 2 + 4))
    color = (r, g, b)

    # Fade effect (alpha oscillation)
    alpha = int(128 + 127 * math.sin(time_elapsed * 3))

    # Scale effect (pulsating size)
    scale_factor = 1 + 0.1 * math.sin(time_elapsed * 4)
    scaled_font = pygame.font.Font(None, int(40 * scale_factor))

    # Render text
    text_surface = scaled_font.render(text, True, color)
    text_surface.set_alpha(alpha)

    # Center text
    x = width  // 2
    y = height // 2 
    
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

FRAMES_PER_SECOND = 30

def fade_in(window,surface, rect, color, speed,clock,fnt,text):
    '''Perform a fade-in effect on a given surface.'''
    for alpha in range(0, 255, speed):
        surface.fill(color)
        window.fill((0,0,0))
        surface.set_alpha(alpha)
        window.blit(surface, rect)

        t = fnt.render(text, True, (255,0,0))
        window.blit(t,(100,100))

        pygame.display.update()
        clock.tick(FRAMES_PER_SECOND)

def fade_out(window,surface, rect, color, speed,clock,fnt,text):
    '''Perform a fade-out effect on a given surface.'''
    for alpha in range(255, -1, -speed):
        surface.fill(color)
        surface.set_alpha(alpha)
        window.fill((0,0,0))
        window.blit(surface, rect)

        t = fnt.render(text, True, (255,0,0))
        window.blit(t,(100,100))

        pygame.display.update()
        clock.tick(FRAMES_PER_SECOND)

