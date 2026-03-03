import pygame
import random
import os
import time
import sys
import configparser

from field      import Field
from block      import *
from settings   import *
from controls.button     import Button
from controls.checkbox   import Checkbox
from controls.checkGroup import CheckGroup
from controls.controls   import Control
from lib                 import * 

class GameSummary:
    def __init__(self):
        self.highest_level = 0
        self.total_games   = 0
        self.highest_score = 0
        self.avg_level     = 0.0
        self.avg_score     = 0.0

class Game:
    ABOUT_IMAGE = "tetris.gif"

    MODE_INFO     = 0
    MODE_ABOUT    = 1
    MODE_HELP     = 2
    MODE_SETTINGS = 3

    REG_FPS  = 3
    FAST_FPS = 20
    FPS_LEVEL_VELOCITY = 2
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption(APP_NAME)
        icon = pygame.image.load(os.path.join(ASSET_FOLDER,self.ABOUT_IMAGE))
        pygame.display.set_icon(icon)
        
        self.clock      = pygame.time.Clock()
        self.FPS        = self.REG_FPS
        self.field      = Field()
        self.running    = True
        self.score      = 0
        self.block      = None
        self.next_block = -1

        self.total_items= 0
        self.total_rows = 0
        self.level_rows = 0
        self.level      = 0
        
        self.summary = {
            0:GameSummary(),
            1:GameSummary(),
            2:GameSummary()
        }
     
        self.is_paused  = False

        self.big_text_font  = pygame.font.SysFont(FONTS, 18,bold=True,italic = True )
        self.info_text_font = pygame.font.SysFont(FONTS, 16,bold=True)
        self.small_text_font= pygame.font.SysFont(FONTS, 14,bold=True,italic = True)
      
        self.projection = None
        self.is_sound = True
        self.is_background_music = False
        self.is_play_mode = False
        self.size_index = 0
        self.bk_index   = 0
       
        self.background = ['None']
        self.background_img = {0:None}
       
        self.load_backggounds()
        self.read_config()
        self.set_field_size()

        #self.field_rect= pygame.Rect(0,0,x,WINDOW_HEIGHT)
        self.info_rect = pygame.Rect(INFO_X,INFO_Y, INFO_CELLS_WIDTH *CELL_SIZE, WINDOW_HEIGHT - INFO_Y * 2) 
        #
        self.rotate_sound    = pygame.mixer.Sound(os.path.join(FOLDER_SOUNDS,"rotate.ogg"))
        self.clear_row_sound = pygame.mixer.Sound(os.path.join(FOLDER_SOUNDS,"clear.ogg"))
        self.start_sound     = pygame.mixer.Sound(os.path.join(FOLDER_SOUNDS,"start.wav"))
        self.exit_sound      = pygame.mixer.Sound(os.path.join(FOLDER_SOUNDS,"exit.mp3"))
        self.loss_sound      = pygame.mixer.Sound(os.path.join(FOLDER_SOUNDS,"loss.mp3"))
        self.new_lvl_sound   = pygame.mixer.Sound(os.path.join(FOLDER_SOUNDS,"new_level.mp3"))

        self.game_music = None    
     
        Control.BK  = BK

        self.buttons = []
        self.create_buttons()

        self.setting_contols = []
        self.create_setting_controls()

        self.contols = []

        for b in self.buttons:
            self.contols.append(b)
        for c in self.setting_contols:
            self.contols.append(c)

        self.start_time = time.time()
        self.total_plays = 0

        self.prompt = ""
        self.prompt_time = time.time()

        self.items_counts = [0,0,0,0,0,0,0,0]     
        self.mode = self.MODE_INFO
  
    def start_game_music(self):
        if self.is_background_music:
            if self.game_music == None:
                self.game_music  = pygame.mixer.Sound(os.path.join(FOLDER_SOUNDS,'game_music.wav'))
                self.game_music.set_volume(0.01)
            self.game_music.play(loops = -1)
            return True

    def load_backggounds(self):
        i = 0
        for folder_path, _, image_names in os.walk(os.path.join(ASSET_FOLDER, BK_FOLDER)):
            for image_name in image_names:
                full_path = os.path.join(folder_path, image_name)
                img = pygame.image.load(full_path).convert_alpha()
                i += 1
                short_name = image_name.split('.')[0]
                self.background.append(short_name)
                self.background_img[i] = img 

    def set_field_size(self):
        self.field.backgroundImage = self.background_img[self.bk_index]      
        (cols,rows) = COLS_ROWS[self.size_index]
        self.field.set_sizes(rows,cols)

    def sound_from_settings(self,source):
        self.is_sound = self.chk_sound.checked

    def bk_music_from_settings(self,source):
        self.is_background_music = self.chk_mk_music.checked

    def create_setting_controls(self):
        x = self.info_rect.left + CELL_SIZE * 4 
        y = self.buttons[0].rect.bottom + CELL_SIZE 

        self.chk_sound = Checkbox((x,y),"Sound",self.is_sound)
        self.chk_sound.func = self.sound_from_settings
        self.chk_sound.hide = True
        self.setting_contols.append(self.chk_sound)
        y = self.chk_sound.rect.bottom
        y += 4

        self.chk_mk_music = Checkbox((x,y),"Backround music",self.is_background_music)
        self.chk_mk_music.func = self.bk_music_from_settings
        self.chk_mk_music.hide = True
        self.setting_contols.append(self.chk_mk_music)
        y = self.chk_mk_music.rect.bottom

        y += CELL_SIZE * 2
        sizes = []
        for key in SIZES.keys():
            sizes.append(SIZES[key])
        self.sizeGroup = CheckGroup(sizes,self.size_index,x,y,"Sizes")

        for chk in self.sizeGroup.chk_boxes:
            chk.hide = True
            self.setting_contols.append(chk)

        y = self.sizeGroup.rect.bottom
        y += 16
        self.bkGroup = CheckGroup(self.background,self.bk_index,x,y,"Background")

        for chk in self.bkGroup.chk_boxes:
            chk.hide = True
            self.setting_contols.append(chk)

    def create_buttons(self):
        W_BUTTON = 116
        H_BUTTON = 48
        D_H = 18

        x_button = self.info_rect.left + (self.info_rect.width -  W_BUTTON)//2 + W_BUTTON/2
        y_button = self.field.yTop + H_BUTTON // 2

        imgBack = pygame.image.load(os.path.join(ASSET_FOLDER,'cancel.png')).convert_alpha()
        btnBack = Button(position=(x_button, y_button),  size=(W_BUTTON, H_BUTTON),  func=self.back, text='Back',image=imgBack)
        btnBack.hide  = True
        btnBack.hint  = "Back to main menu" 
        self.buttons.append(btnBack)

        imgStart = pygame.image.load(os.path.join(ASSET_FOLDER,'start.png')).convert_alpha()
        btnStart = Button(position=(x_button, y_button), size=(W_BUTTON, H_BUTTON), func= self.start, text='Start',image = imgStart)
        btnStart.hint  = "Start play the game"
        self.buttons.append(btnStart)

        y_button += H_BUTTON
        y_button += D_H
        imgAbout = pygame.image.load(os.path.join(ASSET_FOLDER,self.ABOUT_IMAGE)).convert_alpha()
        btnAbout = Button(position=(x_button, y_button), size=(W_BUTTON, H_BUTTON), func=self.about, text='About',image=imgAbout)
        btnAbout.hint  = "Show about information"
        self.buttons.append(btnAbout)
       
        y_button += H_BUTTON
        y_button += D_H
        imgHelp  = pygame.image.load(os.path.join(ASSET_FOLDER,"help.png")).convert_alpha()
        btnHelp  = Button(position=(x_button, y_button), size=(W_BUTTON, H_BUTTON), func=self.help, text='Help',image=imgHelp)
        btnHelp.hint  = "Show help information"
        self.buttons.append(btnHelp)
     
        y_button += H_BUTTON
        y_button += D_H
        imgOptions  = pygame.image.load(os.path.join(ASSET_FOLDER,"options.png")).convert_alpha()
        btnOptions  = Button(position=(x_button, y_button), size=(W_BUTTON, H_BUTTON), func=self.change_settings, text='Settings',image=imgOptions)
        btnOptions.hint  = "Change settings"
        self.buttons.append(btnOptions)
  
        y_button += H_BUTTON
        y_button += D_H
        imgExit  = pygame.image.load(os.path.join(ASSET_FOLDER,'exit.png')).convert_alpha()
        btnExit  = Button(position=(x_button, y_button), size=(W_BUTTON, H_BUTTON), func=self.exit_game, text='Exit',image=imgExit)
        btnExit.hint  = "Exit the game"
        self.buttons.append(btnExit)
        
    def back(self):
        if self.mode == self.MODE_SETTINGS:
            f = False
            bk_index = self.bkGroup.selected_index
            if self.bk_index != bk_index:
                f = True
                self.bk_index = bk_index
            

            if self.size_index != self.sizeGroup.selected_index:
                self.size_index = self.sizeGroup.selected_index
                f = True
            
            if f: self.set_field_size() 

        self.mode = self.MODE_INFO
        self.hide_show_buttins()

    def about(self):
        self.mode = self.MODE_ABOUT
        self.hide_show_buttins()

    def help(self):
        self.mode = self.MODE_HELP
        self.hide_show_buttins()

    def change_settings(self):
        self.mode = self.MODE_SETTINGS
        self.hide_show_buttins()

    def hide_show_buttins(self):
        for b in self.buttons:
            b.reset()
            b.hide = not b.hide
 
        for c in self.setting_contols:
            if self.mode == self.MODE_SETTINGS:
                c.hide = False
            else:
                c.hide = True

    def set_prompt(self,txt):
        self.prompt = txt
        self.prompt_time = time.time()

    def draw_prompt(self):
        if len(self.prompt) > 0:
            text = self.info_text_font.render(self.prompt,1,TEXT_COLOR ) 
            y = self.info_rect.bottom - text.get_height() - 20
            x = (self.info_rect.width - text.get_width())//2
            x += self.info_rect.left
            self.screen.blit(text,(x,y))

    def check_prompt(self):
        if len(self.prompt) > 0:
            now = time.time()
            if now - self.prompt_time > 3:
                self.prompt = ""

    def draw_buttons(self):
        y = 0
        for b in self.buttons:
            if not b.hide:
                yb = b.draw(self.screen)
                if y < yb:
                    y = yb
        return y

    def start(self):
        self.level_rows =  0
        self.level      =  0
        self.next_block = -1
        self.total_items=  0
        self.total_rows =  0
        self.projection = None
        
        self.field.reset()
        self.create_block()

        self.start_time = time.time()
        self.elapsed_time = 0
        self.paused_time  = 0
        self.total_plays += 1
        self.is_paused    = False
        self.is_play_mode = True
        self.FPS = self.REG_FPS

        if not self.start_game_music() :         
            if self.is_sound:
                self.start_sound.play()
            
        for i in range(7):
            self.items_counts[i] = 0
                
    def game_over(self): 
        if self.game_music != None:
            self.game_music.stop()

        self.set_prompt("You lost the game")
        self.is_play_mode = False  
        summary = self.summary[self.size_index]
        
        aLevel = summary.avg_level * summary.total_games
        aLevel += self.level

        aScore = summary.avg_score * summary.total_games
        aScore += self.score
        
        summary.total_games += 1
        
        if summary.highest_level < self.level:
            summary.highest_level = self.level
        
        if summary.highest_score < self.score:
            summary.highest_score = self.score

        summary.avg_level = aLevel / summary.total_games
        summary.avg_score = aScore / summary.total_games
        if self.is_sound:
            self.loss_sound.play()
   

    def exit_game(self):
        self.running = False

    def next_level(self):
        self.level_rows = 0
        self.level     += 1
        self.FPS       += self.FPS_LEVEL_VELOCITY
        self.set_prompt("You pass the level")
        if self.is_sound:
            self.new_lvl_sound.play()

    def get_time(self):
       if self.is_play_mode:
            if not self.is_paused:
                self.elapsed_time = time.time() - self.start_time  -  self.paused_time

    def pause(self):
        self.pause_started = time.time()
        self.is_paused = True

    def resume(self):
        self.paused_time += (time.time() - self.pause_started)
        self.is_paused = False

    def create_block(self):
        n = 6
        if self.next_block >= 0:
            i = self.next_block
        else:
            i = random.randint(0,n)
            
        cell_size = self.field.cell_size
        self.next_block = random.randint(0,n)
        if i == 0:
            self.block = BlockI(cell_size)
        elif i == 1:
            self.block =  BlockO(cell_size)
        elif i == 2:
            self.block =  BlockT(cell_size)
        elif i == 3:
            self.block = BlockJ(cell_size)
        elif i == 4:
            self.block = BlockL(cell_size)
        elif i == 5:
            self.block = BlockS(cell_size)
        elif i == 6:
            self.block = BlockZ(cell_size)
        else:
            print(f"Fatal error - invalid block {i}")
            self.block = None
            return

        if self.block.is_collided(self.field,0,0):
            self.block = None
        else:
            self.total_items += 1
            self.items_counts[i] += 1

    def drawPreview(self,y):
        if self.next_block >= 0:
            y += CELL_SIZE
            i = self.next_block
            dy = 32
            dx = 32
            y += 16
            r = self.draw_item(y,i,self.field.cell_size).inflate(dx,dy)
            r.top  -= dy/4 
            r.left -= dx/4
            self.draw_box_caption("Next",self.small_text_font,r)
            return r
        return None

    def drawItemsTotals(self,r):
        y = r.bottom
        y += 16
        cell_size = 12
        y_min = y
        width = 0
        for i in range(7):
            count = self.items_counts[i]
            y += 12
            r = self.draw_item(y,i,cell_size)
            t = self.small_text_font.render(f"{count}",1, BLACK)
            tw = t.get_width()
            self.screen.blit(t,(r.right,r.centery))
            y = r.bottom + 4
            if width < r.width:
                width = r.w
            
        width += tw 
        width += 40

        x = self.info_rect.left + (self.info_rect.width - width) // 2

        r = pygame.Rect(x,y_min,width,y - y_min)
        self.draw_box_caption("Item counts",self.small_text_font,r)
        return y
   
    def draw_item(self,y,i,cell_size):
        cells = [] 
        if i == 0:
            cells = BlockI.CELLS[0]
        elif i == 1:
            cells = BlockO.CELLS[0]
        elif i == 2:
            cells = BlockT.CELLS[0]
        elif i == 3:
            cells = BlockJ.CELLS[0]
        elif i == 4:
            cells = BlockL.CELLS[0]
        elif i == 5:
            cells = BlockS.CELLS[0]
        elif i == 6:
            cells = BlockZ.CELLS[0]


        yMax = 0
        xMax = 0
        for (r,c) in cells:
            xd = c * cell_size
            yd = r * cell_size
            if yd > yMax:
                yMax = yd
            if xd > xMax:
                xMax = xd

        x = self.info_rect.left + (self.info_rect.width - xMax) // 2
        
        for (r,c) in cells:
            xd = x + c * cell_size
            yd = y + r * cell_size
            pygame.draw.rect(self.screen, COLORS[i]   ,(xd,yd,cell_size,cell_size))
            pygame.draw.rect(self.screen, BLOCK_BORDER,(xd,yd,cell_size,cell_size),1)  
            

        return pygame.Rect(x,y,xMax+cell_size,yMax + cell_size)      

   

    def draw_summary(self,y):
        source= f"""
Items: {self.total_items}
Rows:  {self.total_rows}
Score: {self.score}
Level: {self.level + 1}
"""       
        #return self.draw_text(source,y)
        return self.draw_text_border(source,y)

    def draw_about(self,y):
        source= f"""
{APP_NAME}
Version: {VERSION}
Made By: {AUTHOR}
"""     
        return self.draw_text(source,y,self.big_text_font)  

    def draw_statistics(self,y):
        summary = self.summary[self.size_index]
        source= f"""
Statistics
Board: {SIZES[self.size_index]}
-------------------------
Total games: {summary.total_games}
High  level: {summary.highest_level}
Hight score: {summary.highest_score}
Avg   Level: {round(summary.avg_score,2)}
Avg   score: {round(summary.avg_score,2)}
"""     
        return self.draw_text(source,y,self.small_text_font)  
    
    def draw_help(self,y):
        source= f"""
ESC        - Pause
Left  or A - Move left
Right or D - Move right
Up    or W - Rotate
S          - Reverse rotate
Space - Hard drop
"""     
        return self.draw_text(source,y,self.small_text_font)  

    def draw_text(self,source,y,fnt = None):
        if fnt == None:
            text_surf = self.info_text_font.render(source,1,TEXT_COLOR) 
        else:
            text_surf = fnt.render(source,1,TEXT_COLOR) 

        x = self.info_rect.left + (self.info_rect.width - text_surf.get_width ())//2
  
        self.screen.blit(text_surf,(x,y))
        return y + text_surf.get_height()

    def draw_text_border(self,source,y,fnt = None):
        if fnt == None:
            text_surf = self.info_text_font.render(source,1,TEXT_COLOR) 
        else:
            text_surf = fnt.render(source,1,TEXT_COLOR) 

        x = self.info_rect.left + (self.info_rect.width - text_surf.get_width ())//2
        #text_rect = text_surf.get_frect(center = (x,y))
        text_rect = text_surf.get_frect(topleft = (x,y))
        self.screen.blit(text_surf,text_rect)     
        text_rect = text_rect.inflate(20,16)
        #text_rect = text_rect.move(0,8)
        pygame.draw.rect(self.screen,INFO_BORDER_COLOR, text_rect,INFO_BORER_SIZE,INFO_BORER_RADIUS)
        return y + text_surf.get_height()

    def draw_box_caption(self,caption,fnt,rect):        
        if fnt == None:
            text_surf = self.info_text_font.render(caption,1,TEXT_COLOR) 
        else:
            text_surf = fnt.render(caption,1,TEXT_COLOR) 
        draw_box_with_label(self.screen,rect,text_surf,INFO_BORDER_COLOR)


    def draw_settings(self):
        for c in self.setting_contols:
            c.draw(self.screen)

        self.sizeGroup.draw_panel(self.screen)
        self.bkGroup.draw_panel(self.screen)

    def draw(self):
        self.screen.fill(BK)
        
        #self.screen.blit(self.imgBK,(0,0))
        #pygame.draw.rect(self.screen,BLACK,self.field_rect)
        self.field.draw(self.screen)

        if self.block != None:
            self.block.draw(self.screen,self.field)
         
  
        if self.projection != None:
            self.field.draw_cells_border(self.screen,self.projection,PROJECTTION_COLOR)

        if self.is_play_mode:
            y = self.draw_summary(self.info_rect.top + CELL_SIZE)
            y += CELL_SIZE
            r = self.drawPreview(y)        
            if self.is_paused:
                if r != None:
                    y = r.bottom
                y += 4 * CELL_SIZE
                pause_text = """
Game is paused

Click on ESC 
   to stop play

Click any other key
   to resume play
"""
                self.draw_text(pause_text,y,self.big_text_font)
            elif r != None:
                y = self.drawItemsTotals(r)
   
            y = self.info_rect.bottom - 20
            self.draw_text_border(f'{round(self.elapsed_time)}'.strip(),y)
        else:
            y = self.draw_buttons()
            if self.mode == self.MODE_ABOUT:
                y = self.draw_about(y)
                self.draw_statistics(y)
            elif self.mode == self.MODE_HELP:
                self.draw_help(y)
            elif self.mode == self.MODE_SETTINGS:
                self.draw_settings()
                
        self.draw_prompt()
        pygame.display.update()

    def step(self):   
        if  self.is_paused: return 
        if not self.block.move(self.field):
            if self.FPS == self.FAST_FPS:
                self.FPS = self.REG_FPS
            self.create_block()
            if self.block == None:
                self.game_over()
        else:
            removed_rows = self.field.clear_full_rows()
            if removed_rows > 0: 
                n = len(SCORES)
                if removed_rows >= n:
                     self.score += SCORES[n-1]
                else:
                    self.score += SCORES[removed_rows]

                self.total_rows += removed_rows
                self.level_rows += removed_rows
                if self.level_rows >= 10:
                    self.next_level()                    
                else:
                    if self.is_sound:
                        self.clear_row_sound.play()
                    self.set_prompt(f"{removed_rows} rows removed")

        if self.block != None:
            self.projection = self.block.get_path(self.field)
            #print(self.projection)
        self.check_prompt()

    def rotate(self):
        self.block.turn()
        if self.is_sound:
            self.rotate_sound.play()

    def rotate_back(self):
        self.block.turn_back()
        if self.is_sound:
            self.rotate_sound.play()

    def run(self):
        while self.running:
            if self.is_play_mode:
                self.clock.tick(self.FPS)  
            else:
                self.clock.tick()  

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 
                
                elif event.type == pygame.KEYDOWN:
                    if self.is_play_mode:
                        if self.is_paused:
                            if event.key == pygame.K_ESCAPE:
                                self.is_play_mode = False
                            else:
                                self.resume()
                        elif event.key == pygame.K_UP  or event.key == pygame.K_w:
                            self.rotate()
                        elif event.key == pygame.K_s:
                            self.rotate_back()
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            self.block.move_horizontal(self.field,-1)
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            self.block.move_horizontal(self.field,1)
                        elif event.key == pygame.K_ESCAPE:
                            self.pause()
                        elif event.key == pygame.K_SPACE:
                            self.FPS = self.FAST_FPS
                    else:
                         if event.key == pygame.K_SPACE:
                             self.start()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()   
                        for c in self.contols:
                            if not c.hide:
                                if c.update(True,pos):
                                    break
                        
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        for c in self.contols:
                            if not c.hide:
                                if c.update(False,pos):
                                    break

            if self.is_play_mode:
                self.step()
                self.get_time()
            #Draw
            self.draw()
        #
        # End of game
        #
        if self.is_sound:
            self.exit_sound.play()
        self.save_config()
        self.show_exit_message()
        pygame.quit()
        sys.exit()

    
    def show_exit_message(self): 
        source = f"""
 It was fun to play with you, 
 but now it's time to say
 Goodbye  
         """
        font_size = 24
        if self.total_plays == 0:
            source = "Goodbye"
            font_size = 40
        fade_font  = pygame.font.SysFont(FONTS, font_size,bold=True,italic = True )
        fade_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        fade_surface_rect = fade_surface.get_rect()
  
        
        # Black screen to start with
        self.screen.fill(BLACK)
        pygame.display.update()

        # Fade in to white screen
        fade_in(self.screen,fade_surface, fade_surface_rect, WHITE, 5,self.clock,fade_font,source)
        pygame.time.wait(1000) # Wait for 1 second
        
        # Fade out to black screen
        #fade_out(self.screen,fade_surface, fade_surface_rect, WHITE, 5,self.clock,fade_font,source)
        #pygame.time.wait(1000) # Wait for 1 second

    def save_config(self):
        file_path = os.path.join(DATA_FOLDER,SETTINGS_FILE)
        config = configparser.ConfigParser()
        config[SECTION_GENERAL] = {
            KEY_SOUND   : self.is_sound, 
            KEY_SIZE    : self.size_index,
            KEY_BK      : self.bk_index,
            KEY_BK_MUSIC: self.is_background_music
        }
     
        for i in range(len(SIZES)):
            summary = self.summary[i]
            section = f"size_{i}"
            if not config.has_section(section):
                config.add_section(section)
            config.set(section, KEY_TOTAL_GAMES, f"{summary.total_games}")
            config.set(section, KEY_HIGHT_LEVEL, f"{summary.highest_level}" )
            config.set(section, KEY_HIGHT_SCORE, f"{summary.highest_score}")  
            config.set(section, KEY_AVG_LEVEL  , f"{summary.avg_level}"  )  
            config.set(section, KEY_AVG_SCORE  , f"{summary.avg_score}"  )  

        os.makedirs(DATA_FOLDER, exist_ok=True)  
        with open(file_path, 'w') as configfile:
            config.write(configfile)

    def read_config(self):
        file_path = os.path.join(DATA_FOLDER,SETTINGS_FILE)
        if not os.path.isfile(file_path):
            self.save_config()
            return
        config = configparser.ConfigParser()
        config.read(file_path)

        section = SECTION_GENERAL
        if config.has_option(section,KEY_SOUND):
            self.is_sound   = config.getboolean(section, KEY_SOUND , fallback=self.is_sound )
        if config.has_option(section,KEY_BK_MUSIC):
            self.is_background_music  = config.getboolean(section, KEY_BK_MUSIC , fallback=self.is_background_music )
        if config.has_option(section,KEY_SIZE):
            self.size_index = config.getint(section,KEY_SIZE   , fallback=self.size_index)
        if config.has_option(section,KEY_BK):
            self.bk_index = config.getint(section,KEY_BK   , fallback=self.bk_index)

        for i in range(len(SIZES)):
            summary = self.summary[i]
            section = f"size_{i}"
            if config.has_option(section,KEY_TOTAL_GAMES):
                summary.total_games   = config.getint(section, KEY_TOTAL_GAMES , fallback=summary.total_games)
            if config.has_option(section,KEY_HIGHT_LEVEL):
                summary.highest_level   = config.getint(section, KEY_TOTAL_GAMES , fallback=summary.highest_level)
            if config.has_option(section,KEY_HIGHT_SCORE):
                summary.highest_score   = config.getint(section, KEY_HIGHT_SCORE , fallback=summary.highest_score)
            if config.has_option(section,KEY_AVG_LEVEL):
                summary.avg_level   = config.getfloat(section, KEY_AVG_LEVEL , fallback=summary.avg_level)
            if config.has_option(section,KEY_AVG_SCORE):
                summary.avg_score   = config.getfloat(section, KEY_AVG_SCORE , fallback=summary.avg_score)

if __name__ == '__main__':
    game = Game()
    game.run() 