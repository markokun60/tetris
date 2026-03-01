from turtle import right
import pygame
from controls.controls import Control
from controls.checkbox import Checkbox

class CheckGroup:
    CLR_PANEL = (0,122,122)
    DY = 5
    def __init__(self,options,cur_choice,x,y,caption = None,name=''):
        self.selected_index = cur_choice
        if caption == None:
            self.txt_surf = None
        else:
            font = pygame.font.SysFont(Control.FONT, 16) 
            self.txt_surf = font.render(caption, 1, (0,0,0))
        self.chk_boxes = [] 

        xLeft = x
        yTop  = y
        x += 5
        if self.txt_surf != None:
            y += self.txt_surf.get_height() / 2

        width = 0 if self.txt_surf == None else self.txt_surf.get_width()
        i = 0
        for choice in options:
            checked = True if i == cur_choice else False
            y += self.DY
            chk = Checkbox((x,y),choice,checked,f'{name}_{i}')
            chk.is_auto_check = False
            chk.func = self.on_select
            self.chk_boxes.append(chk)

            y = chk.rect.bottom
            w =  chk.get_width()
            if width < w:
                width = w
            i += 1

        self.rect = pygame.Rect(xLeft,yTop,width+16,y - yTop+16)
    
    def draw_panel(self,screen):
        if self.txt_surf == None:
            pygame.draw.rect(screen,self.CLR_PANEL,self.rect,1)

        else:
            dx = 4
            x = self.rect.left + dx
            y = self.rect.top
            lines = [
                (self.rect.left,y),
                (x,y)
            ]
            lines1 = [
                (x + self.txt_surf.get_width(),y),
                (self.rect.right,y)
            ]
            pygame.draw.rect(screen,self.CLR_PANEL,self.rect,1)
            pygame.draw.line(screen,Control.BK    ,(self.rect.left,self.rect.top),(self.rect.right,self.rect.top),1)
            pygame.draw.lines(screen,self.CLR_PANEL, False, lines , 1)
            pygame.draw.lines(screen,self.CLR_PANEL, False, lines1, 1)

            y -= self.txt_surf.get_height() /2
            screen.blit(self.txt_surf,(x,y))

    def on_select(self,x):
        i = 0
        for chk in self.chk_boxes:
            if chk.name == x.name:
                chk.checked = True
                self.selected_index = i
            else:
                chk.checked = False
            i += 1




