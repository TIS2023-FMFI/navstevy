# About this project

This project addresses visit tracking at a logistics center branch. Before this project, visits were recorded on physical paper sheets. The goal of this project was to create a computer application that would communicate with a tablet, where a security presentation for the visit would be launched. The visit confirms the branch rules by signing. In addition to communication, the application also handles exporting visit data to readable files on the disk.

```
pip install pyinstaller
pip install customtkinter
pip install CTkTable
```

# Installation PC 

From the root, run in cmd, this will create a .exe file in /dist

```
pyinstaller --onefile --windowed --noconsole --icon=src/files/icons/icon.ico src/GUI.py
```

# Installation Android
Build src/TabletApp in *AndroidStudio*


# Final product
The exported final product (PC application + Tablet application) can be found in /Final Product

