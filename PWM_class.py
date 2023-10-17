import os

#Note on initializing pwm. Use these lines
#sudo ldto enable pwm-{x} (pwm-ef)
#echo {0,1} | sudo tee /sys/class/pwm/pwmchip{n}/export (echo 0 |.../pwmchip0/export... should be pwmchip0 if this is the first initialized...)
class pwm:
    def __init__(self,path,period,duty_cycle):
        self.path = path
        self.period = period
        self.duty_cycle = duty_cycle
        os.system("echo "+str(period)+" > "+path+"/period")
        os.system("echo "+str(duty_cycle)+" > "+path+"/duty_cycle")
    def on(self):
        os.system("echo 1 > "+self.path+"/enable")
    def off(self):
        os.system("echo 0 > "+self.path+"/enable")