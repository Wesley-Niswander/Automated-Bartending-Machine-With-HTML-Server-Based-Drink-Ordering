# Automated-Bartending-Machine-With-HTML-Server-Based-Drink-Ordering
Automated bartending machine which can pour 21 separate drinks. Users place orders through an embedded web server accessible via QR code on their smart phones. They then interact with a UI at the machine to initiate their order.

Overview


Main GUI

<img width="526" alt="image" src="https://github.com/Wesley-Niswander/Automated-Bartending-Machine-With-HTML-Server-Based-Drink-Ordering/assets/147947724/5eb500ab-b180-4fff-b682-8d4a9a28c6c5">

The graphical user interface (gui) allows users to start orders placed through the machine's built-in HTML ordering system. The gui contains two buttons. The first button is labeled 'Get next order' and is used to retrieve the next order in the order queue. When pressed the order name and drink are displayed. At this point a cup can be placed on the platform and the 'Order up!' button can be pressed to trigger the machine to begin making the order. The gui also contains a QR code which can be scanned to open the HTML ordering system in a users smart phone.

The machine's user interface was built using PYQT5 and [QT Designer]([url](https://doc.qt.io/qt-6/qtdesigner-manual.html)). QT Designer was used to generate the .ui and .qrc files defining the interface layout. These were converted to Python (.py) files using the [pyuic5 tool]([url](https://pypi.org/project/pyuic5-tool/)). The interface is imported into 'Main GUI.py' where its' handler functions are defined. There are only two handlers which respond to clicking of the two buttons.

The 'Get next order' button handler requests data from the embedded server which returns information on the next order (if available). The 'Order up!' button handler creates and starts a seperate thread for running the physical hardware. This is accomplished using the runBarvis function and hardwareThread class. The runBarvis function loads the recipe file and runs through the sequence of steps to make the drink. The hardwareThread class is a decorator for runBarvis which inherits from Thread. Its' purpose is to make runBarvis non-blocking and to help restrict multiple instantiations of itself. This keeps the gui responsive while preventing multiple orders from running at once. 

HTML Server Ordering

<img width="185" alt="image" src="https://github.com/Wesley-Niswander/Automated-Bartending-Machine-With-HTML-Server-Based-Drink-Ordering/assets/147947724/9f86221b-ce3b-481b-9fe8-ff967817b160">

![image](https://github.com/Wesley-Niswander/Automated-Bartending-Machine-With-HTML-Server-Based-Drink-Ordering/assets/147947724/3fdeeb46-c249-4180-ae62-a6ca25e18647)

![image](https://github.com/Wesley-Niswander/Automated-Bartending-Machine-With-HTML-Server-Based-Drink-Ordering/assets/147947724/2311271f-287a-45e8-8e60-ef06a45c4f44)

Machine Operation

![image](https://github.com/Wesley-Niswander/Automated-Bartending-Machine-With-HTML-Server-Based-Drink-Ordering/assets/147947724/7f8ca5e3-8ab0-434c-a4c5-3c5a8da1d8f0)

<img width="188" alt="image" src="https://github.com/Wesley-Niswander/Automated-Bartending-Machine-With-HTML-Server-Based-Drink-Ordering/assets/147947724/abe5505a-3dc4-4a68-91d5-5d3b3f801cf0">
