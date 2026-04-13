from re import S
from turtle import right
import pygame
import random
import os
import time
import sys
import configparser
from importlib.resources import files


from field      import Field
from block      import *
from settings   import *
from forms      import MainForm,FormOptions
from lib        import * 
from controls.controls   import *

class GameSummary:
    def __init__(self):
        self.highest_level = 0
        self.total_games   = 0
        self.highest_score = 0
        self.avg_level     = 0.0
        self.avg_score     = 0.0

class Game:
    ABOUT_IMAGE = "tetris.png"

    Y_FROM_BOTTOM_FOR_BOX_TIME = 20
    MAX_FPS_GROW_LEVEL = 29
    REG_FPS  = 3
    FAST_FPS = 20
    FPS_LEVEL_VELOCITY = 1
    ROWS_PER_LEVEL = 10

    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.resource_folder = get_resource_path()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption(APP_NAME)
        icon = pygame.image.load(os.path.join(self.resource_folder,IMAGE_FOLDER,Game.ABOUT_IMAGE))
        pygame.display.set_icon(icon)
        
        self.clock      = pygame.time.Clock()
        self.FPS        = self.REG_FPS
        self.field      = Field()
        self.running    = True
        self.score      = 0
        self.block      = None
        self.next_block_size = 1
        self.next_blocks  = []
        self.garbage_rows = 0

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
      
        self.projection   = None
        self.is_sound     = True
        self.is_background_music = False
        self.is_play_mode = False
        self.is_hold      = False

        self.is_lock_delay= False
        self.lock_time = None

        self.size_index = 0
        self.bk_index   = 0
       
        self.background = ['None']
        self.background_img = {0:None}
        self.user_name = ''
       
        self.load_backggounds()
        self.read_config()
        self.set_field_size()

        #self.field_rect= pygame.Rect(0,0,x,WINDOW_HEIGHT)
        self.info_rect = pygame.Rect(INFO_X,INFO_Y, INFO_CELLS_WIDTH *CELL_SIZE, WINDOW_HEIGHT - INFO_Y * 2)  
        #
        self.rotate_sound    = pygame.mixer.Sound(os.path.join(self.resource_folder,SOUND_FOLDER,"rotate.ogg"))
        self.clear_row_sound = pygame.mixer.Sound(os.path.join(self.resource_folder,SOUND_FOLDER,"clear.ogg"))
        self.start_sound     = pygame.mixer.Sound(os.path.join(self.resource_folder,SOUND_FOLDER,"start.wav"))
        self.exit_sound      = pygame.mixer.Sound(os.path.join(self.resource_folder,SOUND_FOLDER,"exit.mp3"))
        self.loss_sound      = pygame.mixer.Sound(os.path.join(self.resource_folder,SOUND_FOLDER,"loss.mp3"))
        self.new_lvl_sound   = pygame.mixer.Sound(os.path.join(self.resource_folder,SOUND_FOLDER,"new_level.mp3"))

        self.game_music = None    
     
        Control.BK  = BK
        self.main_form     = MainForm(self.field,self)
        self.setting_form  = FormOptions(self)
    
        self.start_time = time.time()
        self.total_plays = 0

        self.prompt = ""
        self.prompt_time = time.time()

        self.items_counts = [0,0,0,0,0,0,0,0]     
        self.mode = MODE_INFO
  
    def set_defalut(self):
        self.is_sound        = True
        self.is_background_music = True
        self.next_block_size = 1
        self.garbage_rows    = 0
        self.is_hold         = False

    def start_game_music(self):
        if self.is_background_music:
            if self.game_music == None:
                self.game_music  = pygame.mixer.Sound(os.path.join(self.resource_folder,SOUND_FOLDER,'game_music.wav'))
                self.game_music.set_volume(0.01)
            self.game_music.play(loops = -1)
            return True

    def load_backggounds(self):
        i = 0
        for folder_path, _, image_names in os.walk(os.path.join(self.resource_folder, BK_FOLDER)):
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
    
    def set_prompt(self,txt):
        self.prompt = txt
        self.prompt_time = time.time()

    def draw_prompt(self):
        if len(self.prompt) > 0:
            text = self.info_text_font.render(self.prompt,1,TEXT_COLOR ) 
            y = self.info_rect.bottom - text.get_height() - Game.Y_FROM_BOTTOM_FOR_BOX_TIME - text.get_height()
            x = (self.info_rect.width - text.get_width())//2
            x += self.info_rect.left
            self.screen.blit(text,(x,y))

    def check_prompt(self):
        if len(self.prompt) > 0:
            now = time.time()
            if now - self.prompt_time > 3:
                self.prompt = ""

    def start(self):
        self.level_rows =  0
        self.level      =  0
        self.next_blocks.clear()
        self.total_items=  0
        self.total_rows =  0
        self.projection = None
        self.hold_item  = None
  
        self.field.reset()
        if self.garbage_rows > 0:
            self.field.fill_garbage(self.garbage_rows)

        for i in range(TOTAL_ITEMS):
            self.items_counts[i] = 0

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
                
    def game_over(self): 
        if self.game_music != None:
            self.game_music.stop()

        self.set_prompt("The game is over")
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

    def next_level(self):
        self.level_rows = 0
        self.level     += 1
        if self.level <= Game.MAX_FPS_GROW_LEVEL:
            self.FPS += Game.FPS_LEVEL_VELOCITY
       
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
        while len(self.next_blocks) <= self.next_block_size:
            i = random.randint(0,n)
            self.next_blocks.append(i)

        i = self.next_blocks.pop(0)
            
        cell_size = self.field.cell_size
       
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
            if IS_DEBUG:
                print(f"Fatal error - invalid block {i}")
            self.block = None
            return

        if self.block.is_collided(self.field,0,0):
            self.block = None
        else:
            self.total_items += 1
            self.items_counts[i] += 1

    def hold(self):
        if self.hold_item == None:
            self.hold_item = self.block
            self.create_block()
        else:
            temp = self.block
            self.block = self.hold_item
            self.hold_item = temp
            
        if self.is_sound:
            self.rotate_sound.play()

    def draw_hold(self,y):
        size = 16
        if self.hold_item != None:
            r = self.draw_item(y +12,self.hold_item.id-1,size)
        
            r.width  += 2 * size
            r.left = self.info_rect.left + (self.info_rect.width - r.width) // 2
            r.height += size
            r.top    = y
        else:
            width = size * 4+12
            left = self.info_rect.left + (self.info_rect.width -  width) // 2
            r = pygame.Rect(left,y,width,size * 2)
            r.top  = y

        self.draw_box_caption("Hold",self.small_text_font,r)
        return r.bottom

    def drawPreview(self,y):
        if len(self.next_blocks) == None:
            return y
        size  = 16
        width = 0
        top   = y
        for i in self.next_blocks:   
            y += 12
            r = self.draw_item(y,i,size)
            y = r.bottom
            if width < r.width:
                width = r.width
   
        r.width  = width + size + size
        r.height = r.bottom - top + size
        r.top    = top 
        r.left   = self.info_rect.left + (self.info_rect.width - r.width) // 2
        self.draw_box_caption("Next",self.small_text_font,r)
        return r.bottom

    def drawItemsTotals(self,y):
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
   
    def draw_item(self,y:int,i:int,cell_size:int):
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
        source = files(RESOURCES).joinpath('help.txt').read_text(encoding='utf-8')

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
        self.setting_form.draw(self.screen)
        #for c in self.setting_contols:
        #    c.draw(self.screen)

        #self.sizeGroup.draw_panel(self.screen)
        #self.bkGroup.draw_panel(self.screen)

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
            y = self.draw_summary(self.info_rect.top + CELL_SIZE//2)
            y += CELL_SIZE
            y += 4

            r = None
            if self.next_block_size != 0:
                y = self.drawPreview(y)            
                y += 14
           
            if self.is_hold:     
                y = self.draw_hold(y) + 4
              
            if self.is_paused:
                y += 4 * CELL_SIZE
                pause_text = """
Game is paused

Click any key
   to resume play
"""
                self.draw_text(pause_text,y,self.big_text_font)
            else:
                y = self.drawItemsTotals(y)
   
            y = self.info_rect.bottom - Game.Y_FROM_BOTTOM_FOR_BOX_TIME
            self.draw_text_border(f'{round(self.elapsed_time)}'.strip(),y)
        else:
            self.main_form.draw(self.screen)
            y = self.main_form.y_info()
            if self.mode == MODE_ABOUT:
                y = self.draw_about(y)
                self.draw_statistics(y)
            elif self.mode == MODE_HELP:
                self.draw_help(y)
            elif self.mode == MODE_SETTINGS:
                self.draw_settings()
                
        self.draw_prompt()
        pygame.display.update()

    def step(self):   
        if self.is_paused: return 
        if self.lock_time != None:
            dt = time.time() - self.lock_time
            if dt >= 10.0:
                self.lock_time = None
                self.create_block()

                if self.block == None:
                    self.game_over()
                
        elif not self.block.move(self.field):
            if self.FPS == self.FAST_FPS:
                self.FPS = self.REG_FPS
            if self.is_lock_delay:
                self.lock_time = time.time()
            else:   
                self.lock_time = None
                self.create_block()

                if self.block == None:
                    self.game_over()
        else:
            removed_rows = self.field.clear_full_rows()
            if removed_rows > 0: 
                n = min(len(SCORES),removed_rows)
                score = SCORES[n-1] * (self.level + 1)
                self.score += score
                self.total_rows += removed_rows
                self.level_rows += removed_rows
                self.set_prompt(f"{removed_rows} rows removed. Score increased by {score}")
                if self.level_rows >= Game.ROWS_PER_LEVEL:
                    self.next_level()                    
                else:
                    if self.is_sound:
                        self.clear_row_sound.play()                  

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
                
                elif not self.is_play_mode:
                    if self.mode == MODE_SETTINGS:
                        self.setting_form.handle_controls_events(event)    
                    self.main_form.handle_controls_events(event)

                elif event.type == pygame.KEYDOWN:
                    if self.is_play_mode:
                        if self.is_paused:
                            self.resume() 
                        elif event.key == pygame.K_ESCAPE:
                            self.pause()  
                        elif event.key == pygame.K_UP  or event.key == pygame.K_w:
                            self.rotate()
                        elif event.key == pygame.K_z:
                            self.rotate_back()
                        elif event.key == pygame.K_LEFT:
                            self.block.move_horizontal(self.field,-1)
                        elif event.key == pygame.K_RIGHT:
                            self.block.move_horizontal(self.field,1)
                        elif event.key == pygame.K_ESCAPE:
                            self.pause()
                        elif event.key == pygame.K_SPACE:
                            self.drop(True)
                        elif event.key == pygame.K_c:
                            if self.is_hold:
                                self.hold()

                elif event.type == pygame.MOUSEMOTION:
                    dx, dy = event.rel  # Relative movement since last event
                    if dx > 0:
                        self.block.move_horizontal(self.field,1)
                        #print("Mouse moved RIGHT")
                    elif dx < 0:
                        self.block.move_horizontal(self.field,-1)
                        #print("Mouse moved LEFT")

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    is_left_mouse = True if event.button == 1 else False
                    if is_left_mouse:
                        self.drop(True)
               
  
            if self.is_play_mode:
                self.step()
                self.get_time()
            else:
                if self.mode == MODE_SETTINGS:
                    self.setting_form.update_controls()    
                self.main_form.update_controls() 
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

    def drop(self,hard:bool):
        self.FPS = self.FAST_FPS
        
    
    def show_exit_message(self): 
        source = f"""
 It was fun to play with you {self.user_name}, 
 but now it's time to say
 Goodbye  
         """
        font_size = 24
        if self.total_plays == 0:
            source = f"Goodbye {self.user_name}"
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
            KEY_SOUND    : self.is_sound, 
            KEY_SIZE     : self.size_index,
            KEY_BK       : self.bk_index,
            KEY_BK_MUSIC : self.is_background_music,
            KEY_USER_NAME: self.user_name,
            KEY_PREVIEW_SIZE: self.next_block_size,
            KEY_GARBAGE   : self.garbage_rows,
            KEY_HOLD      : self.is_hold
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
        if config.has_option(section,KEY_PREVIEW_SIZE):
            self.next_block_size = config.getint(section,KEY_PREVIEW_SIZE   , fallback=self.next_block_size)
        if config.has_option(section,KEY_USER_NAME):
            self.user_name = config.get(section,KEY_USER_NAME)
        if config.has_option(section,KEY_GARBAGE):  
            self.garbage_rows = config.getint(section,KEY_GARBAGE , fallback=self.garbage_rows)
        if config.has_option(section,KEY_HOLD):
            self.is_hold = config.getboolean(section,KEY_HOLD , fallback=self.is_hold)

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


def get_resource_path():
   base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
   return os.path.join(base_path,ASSET_FOLDER)

if __name__ == '__main__':
    game = Game()
    game.run() 