# Bertha2

a program that integrates with a Twitch livestream to take user inputed YouTube videos and play them on custom piano player hardware.


## How the hell this thing works (from malcolm, to Jarvis)

0. run ```pip install -r requirements.txt```
1. Run init.py (this will create needed files and the database)
2. (if testing) Run livestream.py, CLI_request_handler.py, converter.py in !!seperate windows!!!
2. (if not testing) Run livestream.py, twitch_request_handler.py, converter.py in !!seperate windows!!!


## Contributing

* when working on a feature, please add it to the appropriate project and indicate that it is in progress
* when working on a new feature, create a new sub-branch of the appropriate component branch