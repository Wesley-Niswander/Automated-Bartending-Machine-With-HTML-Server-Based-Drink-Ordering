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

The runBarvis function operates as a finite state machine.

|State|Function|
|---|---|
|Load|Loads the recipe data from the .json file associated with the drink name|
|Home|Runs the stepper motor towards the home position while continually checking the limit switch. When the limit switch is hit, the motors current position is set to zero steps|
|GetNext|Retrieves the next ingredient from the recipe data. This is done by iteratively checking all possible key names until an ingredient is found.|
|Move|Drives the stepper motor to move the platform below the valve of the current ingredient.|
|Dispense|Sends the weight to dispense to the Arduino which is opens the valve and monitors the load cell in the platform. Once the target weight is reached, the Arduino closes the valve and reports back to the main computer that the operation is complete|

|Key Variable|Data Type|Purpose|
|---|---|---|
|keys|List|Contains the names of the 12 ingredients used (i.e. "vodka").|
|positions|List|Contains the positions in motor steps of all 12 valves. Index 1 contains the position of the ingredient 1 valve, index 2 of the ingredient 2 valve, etc.|
|valves|List|Contains the valve number corresponding to each ingredient. This is sent to the Arduino. Again Index 1 corresponds with ingredient 1 etc.|
|state|String|Current state of the state machine. Used to sequence operations| 
|recipe|Dictionary|Contains ingredient names (keys) and volumes among other things. Data is loaded into this variable from recipe .json files|
|ingredientNumber|Integer|Used to loop through the keys list. Increments from 0 to 11. If a key is found in the recipe it is used. If ingredientNumber finishes incrementing the runBarvis function finishes.|
|ingredient|String|Contains the name of the current ingredient. Extracted from the recipe (key).|
|volume|Float|Contains the volume to dispense of the current ingredient. Extracted from the recipe (value).|
|positionIndex|Integer|The value of ingredientNumber is retained here. Used for indexing the 'positions' list|

The runBarvis function expects one input, "drink." When called it runs through a series of operations to pour a drink. First it loads the correct .json recipe file and stores the data in the recipes dictionary (Load state). It then homes the platform by driving the stepper motor left until a limit switch is reached and zeroes the motor (Home state). The program then iteratively checks a list of known ingredients ('keys' list) against the recipe ('GetNext' state). When an ingredient is found the program stores the name and volume of the ingredient as well as its' index in the ingredient ('keys') list. The program then uses the index to find the position of the ingredient valve (in steps) from a list of known positions ('positions' list). The program then drives the motor to this valve (Move state). Afterward the volume and index are used to dispense the correct volume. The index is used to pull the valve number from a list of valve numbers. The volume and valve number are sent over uart serial to the Arduino which opens the valve and weighs the dispensing fluid until the target volume (technically weight but 1 fluid ounce ~= 1 weight ounce) is dispensed (Dispensing state). Afterwards the program returns to the GetNext state where it iterates through the ingredient 'keys' list where it left off. If it finds another ingredient it will then proceed again to the 'Move' and then 'Dispense' states. If there are no more ingredients then the platform is centered and the runBarvis function exits.

Note on multithreading: The runBarvis function is not called directly within 'Main Gui.py.' Instead it is run from within an instance of the hardwareThread class. This class inherits from Thread with two main changes. The first is that its' run method is overridden to instead call runBarvis. The obvious implication of this is that the runBarvis function can be run in a seperate thread and not block functionality of the main gui. The second is that a class variable 'running' is introduced. This variable is set to true whenever the run method is first called, and false when it completes. This allows checking of whether an instance of hardwareThread is currently running before running another. Madness would surely ensue if two threads attempted to control one set of hardware.

The physical hardware of the machine is driven by IO exposed by Le Potato's 40 pin header. 

  |Component|Function|Class Definintion|Le Potato Hardware|
  |----------|-----------|--------------------|---|
  |Limit Switch|Platform homing|GPIO_class.py/gpioGET|GPIO chip 1, pin 98|
  |Stepper Motor|Moves platform|Stepper_class.py/step|pwm-ef (enabled as pwmchip0), GPIO chip 1, pin 84, GPIO chip 1, pin 86|
  |Arduino|Handles valves and load cell|Dispensing_Class.py/dispenser|ttyAML6 (uarta)|

It is important to note that some of this hardware doesn't work by default. It is necessary to apply the correct overlays by running 'Overlays.sh.' This contains commands to enable the pwm for the motor, the uart for the Arduino, and set the motor disable pin high (to limit power consumption/heat). This file should be added to crontab so that it runs at boot time. This can be accomplished with the following bash commands (crontab -e) (@reboot sh (insert path here)/Overlays.sh).

Below is a more detailed description of the three main hardware components

Limit Switch
The limit switch is used during the homing state of runBarvis. During this time the plat

Stepper Motor

Arduino

