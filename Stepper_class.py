from GPIO_class import gpio
from PWM_class import pwm
import time
#Note:This code does not actually count steps. Instead it runs a delay that will get the motor approximately
#where it needs to be based on the pwm period. It should be noted that the accuracy of this method is
#partially dependent on yout system and how many processes it is running. i.e. if you have a slow computer
#with many things running this might not work as well. In my particular use case I am performing a routine
#with only a few wide tolerance moves where I am re-homing the motor each time.

class step:
    def __init__(self, dir_chip, dir_pin, sleep_chip, sleep_pin, pwm_path,period,duty_cycle):
        self.period=period
        self.duty_cycle = duty_cycle
        self.dir=gpio(dir_chip,dir_pin)
        self.enab=gpio(sleep_chip,sleep_pin)
        self.pw=pwm(pwm_path,period,duty_cycle)
        self.position = 0
    def move(self,direction, steps, autostop):
        #move the motor some number of steps in a specified direction
        # direction "cw" or "ccw"
        # steps = number of steps to move (approximated by a delay). This takes an integer.
        # autostop. When true the motor will stop once the delay time has lapsed. The reason we don't want this
        #  always on is that it can cause the motor to become very "choppy" or even non-functional for small 
        #  repeated moves (ie in homing routines where you would move one step, check the limit switch, move 
        #  one step, etc)
        # returns motor step position. ccw is positive

        if direction == "ccw": #set direction pin
            #counter clockwise move
            self.dir.high()
            self.pw.on()
            self.position = self.position + steps
            time.sleep(steps*(self.period/1000000000.))
            if autostop == True:
                self.pw.off()
        elif direction == "cw":
            #clockwise move
            self.dir.low()
            self.pw.on()
            self.position = self.position - steps
            time.sleep(steps*(self.period/1000000000.))
            if autostop == True:
                self.pw.off()
        else: #stops the motor
            # This command must be run if autostop is off
            self.pw.off()
        return self.position
    def enable(self,onOff):
        #writes to the enable pin to turn power to the motor off
        if onOff == "on":
            self.enab.low()
        elif onOff == "off":
            self.enab.high()
    def zero(self):
        #zeros the motor position
        self.position = 0
    

        



            
