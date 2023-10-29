# Automated-Bartending-Machine-With-HTML-Server-Based-Drink-Ordering
Automated bartending machine which can pour 21 separate drinks. Users place orders through an embedded web server accessible via QR code on their smart phones. They then interact with a UI at the machine to initiate their order.

-Overview

-System
[Le Potato]([url](https://libre.computer/products/aml-s905x-cc/))

-Main GUI

<img width="526" alt="image" src="https://github.com/Wesley-Niswander/Automated-Bartending-Machine-With-HTML-Server-Based-Drink-Ordering/assets/147947724/5eb500ab-b180-4fff-b682-8d4a9a28c6c5">

The graphical user interface (gui) allows users to start orders placed through the machine's built-in HTML ordering system. The gui contains two buttons. The first button is labeled 'Get next order' and is used to retrieve the next order in the order queue. When pressed the order name and drink are displayed. At this point a cup can be placed on the platform and the 'Order up!' button can be pressed to trigger the machine to begin making the order. The gui also contains a QR code which can be scanned to open the HTML ordering system in a user's smart phone.

The machine's user interface was built using PYQT5 and [QT Designer]([url](https://doc.qt.io/qt-6/qtdesigner-manual.html)). QT Designer was used to generate the .ui and .qrc files defining the interface layout. These were converted to Python (.py) files using the [pyuic5 tool]([url](https://pypi.org/project/pyuic5-tool/)). The interface is imported into 'Main GUI.py' where its' handler functions are defined. There are only two handlers which respond to clicking of the two buttons. The 'Get next order' button handler requests data from the built-in server which returns (if available) the name of the drink and name for the order (i.e. John Smith). The 'Order up!' button handler triggers the physical hardware to dispense a drink based on the drink recipe. This calls a specialized function which runs in a seperate thread to keep the gui responsive. This is covered in more detail later.

-HTML Server Ordering

<img width="185" alt="image" src="https://github.com/Wesley-Niswander/Automated-Bartending-Machine-With-HTML-Server-Based-Drink-Ordering/assets/147947724/9f86221b-ce3b-481b-9fe8-ff967817b160">

![image](https://github.com/Wesley-Niswander/Automated-Bartending-Machine-With-HTML-Server-Based-Drink-Ordering/assets/147947724/3fdeeb46-c249-4180-ae62-a6ca25e18647)

![image](https://github.com/Wesley-Niswander/Automated-Bartending-Machine-With-HTML-Server-Based-Drink-Ordering/assets/147947724/2311271f-287a-45e8-8e60-ef06a45c4f44)

-Machine Operation

![image](https://github.com/Wesley-Niswander/Automated-Bartending-Machine-With-HTML-Server-Based-Drink-Ordering/assets/147947724/7f8ca5e3-8ab0-434c-a4c5-3c5a8da1d8f0)

<img width="188" alt="image" src="https://github.com/Wesley-Niswander/Automated-Bartending-Machine-With-HTML-Server-Based-Drink-Ordering/assets/147947724/abe5505a-3dc4-4a68-91d5-5d3b3f801cf0">

State machine

Multithreading

This is accomplished by instantiating and running an instance of the hardwareThread class. This is a subclass of Thread with two important changes. 1) the run method is overridden to call a specialized function (runBarvis) responsible for driving the physical hardware (motor, valves, etc). This function behaves as a finite state machine

The physical hardware of the machine is driven by IO exposed by Le Potato's 40 pin header. 

  |Component|Function|Class Definintion|Le Potato Hardware|
  |----------|-----------|--------------------|---|
  |Limit Switch|Platform homing|GPIO_class.py/gpioGET|GPIO chip 1, pin 98|
  |Stepper Motor|Moves platform|Stepper_class.py/step|pwm-ef (enabled as pwmchip0), GPIO chip 1, pin 84, GPIO chip 1, pin 86|
  |Arduino|Handles valves and load cell|Dispensing_Class.py/dispenser|ttyAML6 (uarta)|

It is important to note that some of this hardware doesn't work by default. It is necessary to apply the correct overlays by running 'Overlays.sh.' This contains commands to enable the pwm for the motor, the uart for the Arduino, and set the motor disable pin high (to limit power consumption/heat). This file should be added to crontab so that it runs at boot time. This can be accomplished with the following bash commands.
|crontab -e|
|@reboot sh (insert path here)/Overlays.sh|

Below is a more detailed description of the three main hardware components

Limit Switch

Stepper Motor

Arduino

