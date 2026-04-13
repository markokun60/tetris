import pygame
from   typing   import Tuple
from   controls.controls import Control

class Button(Control):
    CLR_BTN_RADIUS   = 5
    CLR_BTN_TEXT = (0,0,0)
    BTN_RADIUS   = 5
 
    def __init__(self, name,position, size, clr=None, cngclr=None, hint_clr=None, func=None, text='',font_name=None, font_size=None,  image = None):

        super().__init__(name,Control.BUTTON,font_name,font_size,func,text,Button.CLR_BTN_TEXT,hint_clr)
        self.image  = image

        if  size[0] == 0:
            w = self.txt_surf.get_width()+ 16
            if self.image != None:
                w += self.image.get_width()
            self.size = (w,size[1])
        else:
            self.size   = size    

        if clr == None:
            self.clr = self.CLR_BTN
        else:
            self.clr = clr
      
        self.surf   = pygame.Surface(self.size)
        self.surf1  = pygame.Surface(self.size)
        self.rect   = self.surf.get_rect(center=position)
      
        if cngclr == None:
            self.cngclr = Control.CLR_BTN_CHNG

        if self.cngclr == None:
            self.cngclr = self.clr

        if len(self.clr) == 4:
            self.surf.set_alpha(clr[3])

        self.txt_rect = self.txt_surf.get_rect(center=[wh//2 for wh in self.size]) 
        self.pressed  = False

        self.draw_surface(self.surf ,self.clr)
        self.draw_surface(self.surf1,self.cngclr)
    
    def reset(self):
        super().reset()
        self.clr      = Control.CLR_BTN
        self.cngclr   = Control.CLR_BTN_CHNG
        self.hint_clr = Control.CLR_HINT
        if self.cngclr == None:
            self.cngclr = self.clr

        self.hint_surf= None
        self.draw_surface(self.surf ,self.clr)
        self.draw_surface(self.surf1,self.cngclr)

    def draw_surface(self, surf, curclr):
        rect = pygame.Rect(0,0,self.rect.width,self.rect.height)
        if self.BTN_RADIUS == 0:
            surf.fill(curclr)
        else:
            surf.fill(self.BK)
            pygame.draw.rect(surf, curclr, (0,0,rect.width,rect.height), border_radius=self.BTN_RADIUS)   
       
        surf.blit(self.txt_surf, self.txt_rect)

        if self.image != None:
            x = rect.x
            y = rect.y + rect.height/2 - self.image.get_height()/2
            surf.blit(self.image,(x,y))
    
    def draw(self, screen):  
        #print(self.rect,self.txt)
        if self.mouseover():
            if pygame.mouse.get_pressed()[0]:
                r = self.rect.copy()
                r.x += 2;
                r.y += 2
                screen.blit(self.surf1, r)
            else:
                screen.blit(self.surf1, self.rect)
                if self.show_hint : 
                    self.draw_hint(screen)
            #self.setActive(True)        
        else:
            screen.blit(self.surf, self.rect)
            #if self.active:
            #    pygame.draw.rect(screen,Control.CLR_SELECTED,self.rect,1)
        return self.rect.bottom         
      
    
    def handle_event(self, event,is_left_mouse:bool, is_double_click:bool, position: Tuple[float, float]):
        self.curclr = self.clr
        if is_left_mouse:
            if self.rect.collidepoint(position):
                self.setActive(True)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.curclr = self.cngclr
                else:
                    self.call_back()
                return True
        return False

    def mouseover(self):
        self.curclr = self.clr
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.curclr = self.cngclr
            return True
        return False

  

   




