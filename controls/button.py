import pygame
from   typing   import Tuple
from   controls.controls import Control

class Button(Control):
    CLR_BTN_RADIUS   = 5

    CLR_BTN      = (220, 220, 220)
    CLR_BTN_CHNG = (255, 0, 0)
    BTN_RADIUS   = 5
  

    def __init__(self, position, size, clr=None, cngclr=None, hint_clr=None, func=None, text='',
                font_name=None, font_size=16, font_clr=[0, 0, 0], image = None):
        super().__init__(font_name,font_size,func,text)
        if clr == None:
            self.clr = self.CLR_BTN
        else:
            self.clr = clr
        self.size   = size
        self.surf   = pygame.Surface(size)
        self.surf1  = pygame.Surface(size)
        self.rect   = self.surf.get_rect(center=position)
        self.image  = image
 
        if cngclr == None:
            self.cngclr = self.CLR_BTN_CHNG

        if self.cngclr == None:
            self.cngclr = self.clr

        if len(self.clr) == 4:
            self.surf.set_alpha(clr[3])

        # text         
        self.font_clr = font_clr
        self.txt_rect = self.txt_surf.get_rect(center=[wh//2 for wh in self.size])
        
        #hints
        self.show_hint = False
        self.hint     = ''
        self.hint_surf= None
        if hint_clr == None:
            self.hint_clr = self.CLR_HINT
        else:
            self.hint_clr = hint_clr
      
        self.pressed  = False

        self.draw_surface(self.surf ,self.clr)
        self.draw_surface(self.surf1,self.cngclr)
    
    def reset(self):
        self.clr      = self.CLR_BTN
        self.cngclr   = self.CLR_BTN_CHNG
        self.hint_clr = self.CLR_HINT
        if self.cngclr == None:
            self.cngclr = self.clr

        self.hint_surf= None
        self.draw_surface(self.surf ,self.clr)
        self.draw_surface(self.surf1,self.cngclr)


    def set_hint(self,hint):
        self.hnt = hint
        if  self.hint_surf == None:
            font_size =  self.font_size - 4
            font_hint = pygame.font.SysFont(self.font_name,font_size)
            self.hint_surf = font_hint.render(self.hint, 1,  self.hint_clr)
        else:
            self.hint_surf = font_hint.render(self.hint, 1, self.hint_clr)

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
            mouse_pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                r = self.rect.copy()
                r.x += 2;
                r.y += 2
                screen.blit(self.surf1, r)
            else:
                screen.blit(self.surf1, self.rect)
                if self.show_hint : 
                    self.draw_hint(screen)
        else:
            screen.blit(self.surf, self.rect)
        return self.rect.bottom         
      
    def draw_hint(self,screen):
        if len(self.hint) > 0 :
            if self.hint_surf == None:
                self.set_hint(self.hint)
            screen.blit(self.hint_surf, (self.rect.x + 8,self.rect.bottom))
    
    def update(self, mousedown: bool, position: Tuple[float, float]):
        self.curclr = self.clr
        if self.rect.collidepoint(position):
            if mousedown:
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

  

   




