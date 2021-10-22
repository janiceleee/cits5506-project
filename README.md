# cits5506-project
# Smart Parking Finder

## Inital Setup
1. `source venv/bin/activate`
2. `sudo apt-get install sqlite`
3. `pip install -r requirements.txt`
4. `flask db init`
5. Initialise database with mock values `python3 database.py`
6. Start webserver with `flask run`
7. Start UDP server with `python3 server.py`



## Caution regarding usage of the sensor and the differences between Client.py and Client_bug.py
- If using Client.py, ensure that after installation, the sensor is __not moved at all__.
Once the initial 21 readings has been used to determine the set of XYZ readings to represent state0: the vacant bay with no interference.
If the sensor is moved, you may never be able to move it back into position and observe the same set of readings again. i.e., the bay will be treated as occupied forever.
This method can only recognise when the bay is not vacant (due to interference) but cannot distinguish between interference caused by a vehicle, or interference caused by other objects.

- If using Client_bug.py, the difference in determining bay vacancy status is that instead of treating the XYZ readings as a set, it simply records the mode of the window of previous X, Y, and Z axis reading and stores it as "previous", and at each epoch, compares the previous reading to the current reading to determine if any change in any of the 3 axis was detected.
Only if change was detected, then will the bay's vacancy status be updated accordingly.
Naturally this method is not very robust and as such is discouraged.
