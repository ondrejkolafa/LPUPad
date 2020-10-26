from cx_Freeze import setup, Executable
import os
import sys

base = None  
if sys.platform == "win32":  
    base = "Win32GUI"

os.environ['TCL_LIBRARY'] = "c:\\Users\\OKolafa\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tcl8.6\\"
os.environ['TK_LIBRARY'] = "c:\\Users\\OKolafa\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tk8.6\\"

includes      = []
include_files = [r"c:\\Users\\OKolafa\\AppData\\Local\\Programs\\Python\\Python36-32\\DLLs\\tcl86t.dll", \
                 r"c:\\Users\\OKolafa\\AppData\\Local\\Programs\\Python\\Python36-32\\DLLs\\tk86t.dll"]


setup(name = "LPUPad" ,
      version = "0.2" ,
      description = "" ,
      options = {"build_exe": {"includes": includes, "include_files": include_files, "optimize": 2}},
      executables = [Executable("LPUPad.py", base=base)]
      )

#===============================================================================
# Z nejakeho duvodu vsem nazvum podadresaru ve slozkach TCL a TK chybi prvni pismenko.
# Je nutne rucne nazvy opravit. Cesta ke vzorum je vyse v os.environ.
#
# Spusteni buildovani: v CMD "python setup.py build"
#===============================================================================



#===============================================================================
# pyinstaller --noconfirm --onefile --nowindow --icon=..\LPUPad.ico LPUPad.spec
#===============================================================================    