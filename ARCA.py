'''
Author name: Caio Moreira Porta
Author email: caio.porta12@gmail.com
'''

import os
import sys


def _locate():
    # PyInstaller onefile/zip bundle: assets sit at the MEIPASS root.
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS, os.path.join(sys._MEIPASS, 'assets')
    ROOT = os.path.dirname(os.path.abspath(__file__))
    # Source checkout: code under src/app, assets under src/assets.
    if os.path.isdir(os.path.join(ROOT, 'src', 'app')):
        return os.path.join(ROOT, 'src', 'app'), os.path.join(ROOT, 'src', 'assets')
    # PyInstaller onedir bundle: modules and 'assets' folder sit next to the exe.
    return ROOT, os.path.join(ROOT, 'assets')


APPS_DIR, ASSETS_DIR = _locate()

sys.path.insert(0, APPS_DIR)
os.chdir(ASSETS_DIR)

from ui.graphical_thread import graphical_thread
import threading

ThreadLock = threading.Lock()

def main():
    mgraphical_thread = graphical_thread()
    mgraphical_thread.run()

if __name__ == '__main__':
    main()
