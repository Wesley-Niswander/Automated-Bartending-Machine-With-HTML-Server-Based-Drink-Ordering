#The gpio class takes a chip number and a pin number then passes
#commands to Linux
# import os
import subprocess
class gpio:
    def __init__(self, chip, pin):
        #Add "set pin high" and "set pin low" commands to class data
        self.highCMD = ['gpioset',str(chip),str(pin)+'=1']
        self.lowCMD = ['gpioset',str(chip),str(pin)+'=0']
    def high(self):
        #set the pin high
        subprocess.run(self.highCMD)
    def low(self):
        #set the pin low
        subprocess.run(self.lowCMD)

class gpioGet:
    def __init__(self, chip, pin):
        #Add "set pin high" and "set pin low" commands to class data
        self.command = ['gpioget', str(chip), str(pin)]
    def get(self):
        #set the pin high
        state = subprocess.run(self.command,capture_output=True)
        return int(state.stdout)