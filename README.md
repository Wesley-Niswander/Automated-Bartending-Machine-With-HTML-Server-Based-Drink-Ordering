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
|ingredientNumber|Integer|Used to loop through the keys list. Increments from 0 to 11. If a key is found in the recipe it is used. If ingredientNumber finishes incrementing the runBarvis function finishes.|
|ingredient|String|Contains the name of the current ingredient. Extracted from the recipe (key).|
|volume|Float|Contains the volume to dispense of the current ingredient. Extracted from the recipe (value).|
|positionIndex|Integer|The value of ingredientNumber is retained here. Used for indexing the 'positions' list|

The function expects one input, 'drink' when called. It consists of some initial setting up of variables before entering a while loop. This while loop runs repeatedly until the operation is complete and the drink is finished. The while loop contains an if, elif statement which continually checks the value of the variable 'state' to perform the appropriate steps in sequence. The initial value of 'state' is "Load." During the load state the recipe .json file sharing the name of the variable 'drink' is loaded into a dictionary named 'recipe.' The 'recipe' dictionary contains key-value pairs with ingredient names and weights. At the end of the "Load" operation 'state' is set to 'Home.' During the homing sequence the stepper motor drives the platform to the left until a limit switch is hit. The postion of the motor is then set to zero steps and 'state' is set to 'GetNext.' During the "get next" state a list of ingredient keys (the 'key' variable) is iteritively checked against the keys in the 'recipe' data. When a key is found the weight value is extracted. The weight and 'key' index (meaning position in 'keys' list) are retained. The state is then set to 'Move.' The 'key' index is used to pull the corresponding valve position in motor steps from the 'positions' list. 


Multithreading

This is accomplished by instantiating and running an instance of the hardwareThread class. This is a subclass of Thread with two important changes. 1) the run method is overridden to call a specialized function (runBarvis) responsible for driving the physical hardware (motor, valves, etc). This function behaves as a finite state machine

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

