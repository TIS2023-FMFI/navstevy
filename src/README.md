This file contains source code for tablet and pc application.

'''
pip install pyinstaller
pip install customtkinter
pip install CTkTable
'''

Installation:
From root navstavy, run in cmd:
'''
pyinstaller --onefile --windowed --noconsole --icon=src/files/icons/icon.ico src/GUI.py
'''
This will create .exe file in /dist