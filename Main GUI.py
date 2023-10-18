import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from main_interface import Ui_Barvis3 
#Import the class generated from qt designer using pyuic5 -o PythonFile.pyy QTDesignerFile.ui
#Also need to generate a resource file (holds image data and stuff) pyrcc5 resources.qrc -o resources.py 
from HardwareThread import hardwareThread
from Print_Drink_Info import printInfo
import requests

#side note on QR code. Uses machines IP address which was set to static
#in a config file accessed by sudo nano /etc/dhcpcd.conf

class Window(QMainWindow, Ui_Barvis3):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.GetNextOrder.clicked.connect(self.getNext)
        self.OrderUp.clicked.connect(self.order)
        
    def getNext(self):
        try:
            order = requests.get("http://127.0.0.1:5000/getNextOrder")
            print(order)
            self.drink = order.json()[u'drink']
            self.name = order.json()[u'name']
            self.orderNumber = order.json()[u'order number']
            print(f"{order.json()}")
        except:
            self.drink = "no new orders"
            self.name = ""
            self.orderNumber = ""
        self.label.setText(self.drink)
        self.label_2.setText(self.name)
        self.label_7.setText(printInfo(self.drink))
        
    def order(self):
        if self.drink != "no new orders":
            print("making order...")
            hardware = hardwareThread()
            if hardware.running:
                print("Machine busy, please wait...")
                msg = QMessageBox()
                msg.setWindowTitle("Barvis")
                msg.setText("Machine busy, please wait...")
                x = msg.exec_()
            else:
                hardware.setDrink(self.drink)
                hardware.start()
        else:
            print("no new orders")
            msg = QMessageBox()
            msg.setWindowTitle("Barvis")
            msg.setText("No new orders!\nTo place an order\nplease scan the QR code.")
            x = msg.exec_()
        
app = QApplication(sys.argv)
win = Window()
win.show()
sys.exit(app.exec())
    
        