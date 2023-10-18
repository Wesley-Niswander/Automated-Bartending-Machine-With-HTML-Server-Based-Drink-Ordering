#The purpose of this class is to run the runBarvis function in a seperate thread.
#runBarvis serves to run the physical hardware (motor, valves, etc) to make the
#drink order. This way runBarvis is not blocking. The reason for making a subclass
#of Thread is to make use of a class variable called running. This way the main
#program can check if the physical hardware is in use before running runBarvis again.

import threading
from Barvis_3 import runBarvis

class hardwareThread(threading.Thread):
    running = False
    def __init__(self):
        super().__init__()
        self.drink = ''

    def setDrink(self,drink):
        self.drink = drink

    def run(self):
        hardwareThread.running = True
        runBarvis(self.drink)
        hardwareThread.running = False
