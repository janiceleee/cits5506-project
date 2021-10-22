# cits5506-project
# Smart Parking Finder

## Initial Setup
1. `source venv/bin/activate`
2. `sudo apt-get install sqlite`
3. `pip install -r requirements.txt`
4. `flask db init`
5. Initialise database with mock values `python3 database.py`

## Launch Server
1. Start webserver with `flask run`
2. Start UDP server with `python3 server.py`

## File Descriptions
-	`README.md`: instructions on how to set up the app. 
-	`requirements.txt`: the names and versions of the libraries that will be installed in the python virtual environment. 
-	`app.py`: This is the central piece of the application, which links all the other files together. It creates the Bay table using Flask Alchemy, defining its columns and column types, as well as a unique integer identifier as primary key. An app route is then defined for the landing page. A route is required for every webpage in a Flask app. The route allows us to create variables for each dynamic item we would like to display on the user interface, and to insert those variables in our index.html template when rendering it. 
-	`client.py`: gets magnetometer readings from Arduino, does a check to see if parking bay is vacant or occupied and sends the information to the server. This should be run on the Raspberry Pi.
-	`server.py`: listens for messages from the sensors and updates the relevant records in the database.
-	`database.py`: inserts information about 9 parking bays, numbered 1-9, in the Bay table. The only bay’s status that is regularly updated based on our sensor’s readings is Bay 1. After adding the parking bay records to the table, we ensure we `commit()` these changes to the database.
-	`Templates/index.html`: The written content and structure of the page to be shown to the user. The date and time of the request in shown on the page, as well as the number of vacant bays and the status of each bay. The parking bays visual representation is made using a grid display, each bay being a grid item. 
-	`Static/Project.css`: Provides styling rules for the `index.html` content. It sets the font size, font family, margin sizes, title colours and alignment. Also, it allows the grid of car bays to be displayed in three rows to mirror a real car park. Each vacant car bay is displayed in green, whereas the occupied ones are in red. 


## Caution regarding usage of the sensor and the differences between Client.py and Client_bug.py
- If using `client.py`, ensure that after installation, the sensor is __not moved at all__.
Once the initial 21 readings has been used to determine the set of XYZ readings to represent state0: the vacant bay with no interference.
If the sensor is moved, you may never be able to move it back into position and observe the same set of readings again. i.e., the bay will be treated as occupied forever.
This method can only recognise when the bay is not vacant (due to interference) but cannot distinguish between interference caused by a vehicle, or interference caused by other objects.

- If using `client_bug.py`, the difference in determining bay vacancy status is that instead of treating the XYZ readings as a set, it simply records the mode of the window of previous X, Y, and Z axis reading and stores it as "previous", and at each epoch, compares the previous reading to the current reading to determine if any change in any of the 3 axis was detected.
Only if change was detected, then will the bay's vacancy status be updated accordingly.
Naturally this method is not very robust and as such is discouraged.
