sudo ldto enable pwm-ef
echo 0 | sudo tee /sys/class/pwm/pwmchip0/export

sudo ldto enable uarta

gpioset 1 86=1