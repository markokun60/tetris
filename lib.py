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

def fade_in(window,surface, rect, color,  speed,clock,fnt,text):
    '''Perform a fade-in effect on a given surface.'''
    for alpha in range(0, 255, speed):
        surface.fill(color)
        window.fill((0,0,0))
        surface.set_alpha(alpha)
        window.blit(surface, rect)

        txt_color = (255,255 - alpha,0) 
        t = fnt.render(text, True, txt_color)
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

        txt_color = (255,255 - alpha,0) 
        t = fnt.render(text, True, txt_color)
        window.blit(t,(100,100))

        pygame.display.update()
        clock.tick(FRAMES_PER_SECOND)


def scale_image_keep_ratio(image, max_width, max_height):
    """Scale an image to fit within max_width and max_height while keeping aspect ratio."""
    original_width, original_height = image.get_size()
    
    # Calculate scaling factor
    ratio = min(max_width / original_width, max_height / original_height)
    
    # Compute new dimensions
    new_width = int(original_width * ratio)
    new_height = int(original_height * ratio)
    
    # Scale the image smoothly
    return pygame.transform.smoothscale(image, (new_width, new_height))

def draw_box_with_label(window,rect,label_surf,color,line_width = 1):
    w = label_surf.get_width()
    x = rect.left +  (rect.width - w)/2

    pygame.draw.line(window,color, (rect.left,rect.top),(x,rect.top),line_width)
    y = rect.top - label_surf.get_height() // 2
    window.blit(label_surf,(x,y))
    x += w
    pygame.draw.line(window,color, (x,rect.top),(rect.right,rect.top))

   
    points = [
        (rect.left ,rect.top),
        (rect.left ,rect.bottom),
        (rect.right,rect.bottom),
        (rect.right,rect.top)
    ]
    pygame.draw.lines(window,color,False,points,line_width)
