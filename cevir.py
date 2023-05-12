import os

try:
    os.system("python -m PyQt5.uic.pyuic -x Spor.ui -o ui_Spor.py")
    
except Exception as e:
    print(e)
    pass