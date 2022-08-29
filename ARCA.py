'''
Author name: Caio Moreira Porta
Author email: caio.porta12@gmail.com
'''

from HMI import graphical_thread
import threading

ThreadLock = threading.Lock()

mgraphical_thread = graphical_thread()
mgraphical_thread.run()