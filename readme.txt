https://www.youtube.com/watch?v=nF_crEtmpBo&t=374s

contols
https://github.com/dmfabritius/PygameControls/tree/main


py -m venv env_games

activate env
env_games\Scripts\Activate.bat

install
pip install pygame-ce
pip install pyinstaller
Create env
py -m venv env_games

activate env
env_games\Scripts\Activate.bat

install
---------------
pip install pygame-ce
pip install pyinstaller

create exe
--------------
pyinstaller --name pyTetris  --onefile -w --icon=tetris.ico --add-data "assets:assets" --add-data "resources:resources"  main.py  
