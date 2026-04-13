from typing import Final
import pygame
from controls.controls import Control
from controls.checkbox import Checkbox

class CheckGroup:
    all_groups = []
    RECT_DX : Final[int] = 16
    DY      :int  = 4
    
    def __init__(self,options,cur_choice,x,y,caption,name,multi_sellect = True,func = None):
        CheckGroup.all_groups.append(self)
        self.selected_index = cur_choice
        self.is_multiselect = multi_sellect    
        self.func = func
        self.caption = caption
        if self.caption == None:
            self.txt_surf = None
        else:
            self.font = pygame.font.SysFont(Control.FONT, Control.FONT_SIZE+2,bold = Control.FONT_BOLD) 
            self.txt_surf = self.font.render(caption, 1, Control.CLR_TEXT)
            
        self.chk_boxes = [] 
        xLeft = x
        yTop  = y
        x += 5
        if self.txt_surf != None:
            y += self.txt_surf.get_height() / 2

        width = 0 if self.txt_surf == None else self.txt_surf.get_width()
        i = 0
        style = Checkbox.STYLE_BOX if self.is_multiselect else Checkbox.STYLE_RADIO
        for choice in options:
            checked = True if i == cur_choice else False
            y += self.DY
            chk = Checkbox(name=f'{name}_{i}',position=(x,y),text= choice,checked=checked,style=style,func= self.on_select)
            chk.is_auto_check = False
            self.chk_boxes.append(chk)

            y = chk.rect.bottom
            w = chk.get_width()
            if width < w:
                width = w
            i += 1

        self.rect = pygame.Rect(xLeft,yTop,width+CheckGroup.RECT_DX,y - yTop+16)
        if Control.form != None:
            Control.form.groups.append(self)
        
    def select(self,index:int):
        i = 0
        for chk in self.chk_boxes:
            if index == i:
                chk.checked = True
            else:
                chk.checked = False
            i += 1

    def reset(self):
        width = 0 
        if self.caption != None:
            self.txt_surf = self.font.render(self.caption, 1, Control.CLR_TEXT) 
            width = self.txt_surf.get_width()

        for chk in self.chk_boxes:
            w = chk.get_width()
            if width < w:
                width = w
        self.rect.width = width + CheckGroup.RECT_DX

    def draw(self,screen):
        clr = Control.CLR_BORDER
        if self.txt_surf == None:
            pygame.draw.rect(screen,clr,self.rect,1)

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
            pygame.draw.rect(screen,clr,self.rect,1)
            pygame.draw.line(screen,Control.BK    ,(self.rect.left,self.rect.top),(self.rect.right,self.rect.top),1)
            pygame.draw.lines(screen,clr, False, lines , 1)
            pygame.draw.lines(screen,clr, False, lines1, 1)

            y -= self.txt_surf.get_height() /2
            screen.blit(self.txt_surf,(x,y))

    def on_select(self,checked):
        i = 0
        selected = Control.selected
        for chk in self.chk_boxes:
            
            if chk.name == selected.name:
                chk.checked = True
                self.selected_index = i
            elif not self.is_multiselect:
                chk.checked = False
            i += 1

        if self.func != None:
            self.func(self.selected_index,checked)

def reset_all_groups():
    for g in CheckGroup.all_groups:
        g.reset()

