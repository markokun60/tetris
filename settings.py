from typing import Final

#Apps
VERSION :Final[str] = "1.0.0"
AUTHOR  :Final[str] = "Mark Okun"
APP_NAME:Final[str]= "Tetris"

ROWS:Final[int] = 36
COLS:Final[int] = 20

M_ROWS:Final[int] = 24
M_COLS:Final[int] = 16

S_ROWS:Final[int] = 20
S_COLS:Final[int] = 10

COLS_ROWS = [(S_COLS,S_ROWS),(M_COLS,M_ROWS),(COLS,ROWS)]

SIZES = {
    0:f'Small  {S_COLS}x{S_COLS}',
    1:f'Medium {M_COLS}x{M_COLS}',
    2:f'Large  {COLS}x{ROWS}'
}

CELL_SIZE:Final[int]= 16
INFO_CELLS_WIDTH    = 16
INFO_X = COLS * CELL_SIZE + CELL_SIZE
INFO_Y = CELL_SIZE

WINDOW_WIDTH  = INFO_X +  INFO_CELLS_WIDTH * CELL_SIZE
WINDOW_HEIGHT = (ROWS+2) * CELL_SIZE

#Colors
DARK_GRAY =( 26, 31, 40)
LIGHT_GRAY=(192,192,192)
RED      = (255,  0,  0)
ORANGE   = (226,118, 17)
YELLOW   = (255,255,  0)
GREEN    = (  0,255,  0)
BLUE     = ( 13,64 ,255)
DARK_BLUE= (44 ,44 ,127)
CYAN     = (0  ,255,255)
WHITE    = (255,255,255)
BLACK    = (  0,  0,  0)
PURPLE   = (128, 0 ,128)   


BK                = (250,250,250)
BLOCK_BORDER      = (212,212,212)
PROJECTTION_COLOR = (137,127,127)
TEXT_COLOR        = BLACK
INFO_BORDER_COLOR = BLACK #(240,240,240)
INFO_BORER_SIZE   = 5
INFO_BORER_RADIUS = 10

COLORS = {
    0: CYAN,       #I
    1: BLUE ,      #O
    2: YELLOW,     #T
    3: RED   ,     #J
    4: ORANGE,     #L
    5: GREEN ,     #S
    6: PURPLE ,    #Z    
}


SCORES = [40,100,300,1200]

FONTS:Final[str]= 'monospace' #'Arial, Helvetica, sans-serif'
FOLDER_SOUNDS:Final[str] = "sounds"
DATA_FOLDER  :Final[str] = "data"
ASSET_FOLDER :Final[str] = "assets"
BK_FOLDER    :Final[str] = "background"

SETTINGS_FILE = "tetris.ini"
SECTION_GENERAL="general"
KEY_SOUND="sound"
KEY_BK_MUSIC="bk_music"
KEY_SIZE ="size"
KEY_BK   ="background"

KEY_TOTAL_GAMES = "total_games"
KEY_HIGHT_LEVEL = "high_level"
KEY_HIGHT_SCORE = "high_score"
KEY_AVG_LEVEL   = "avg_level"
KEY_AVG_SCORE   = "avg_score"
