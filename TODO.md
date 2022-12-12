# Some bigger things to implement

* Easy and consistent testing (even without hardware connected)
  * [DONE] Hardware simulator
  * Documented test setup guide
  * [DONE] Write a script that stress tests the stream
* Better logging, some way of enabling different levels of information without constantly commenting out print statements
  * [DONE] Control general log level, when debugging, debug level logs should be enabled
  * [DONE] Also be able to control log level for each module, when troubleshooting a single module for example, all debug level logs are not needed
  * Make sure the log levels are accurate to what they are. Document how to level logs.
  * Change log level while program is running? https://towardsdatascience.com/how-to-add-a-debug-mode-for-your-python-logging-mid-run-3c7330dc199d
* Be able to pause the program when certain conditions aren't met to prevent undefined behaviours.
  * In the following cases, the program should pause but not crash or stop running:
    * OBS isn't open / crashes / can't be accessed
    * OBS can't find elements that need to be accessed
    * Cannot connect to Twitch chat
    * Cannot connect to hardware / hardware emulator
  * In the following cases the program should stop running:
    * Can't access important secret keys / keys are not valid
* There should be more information displayed on stream as to what is happening with the program and robot
  * [DONE] When there is downtime to cool solenoids, this should be displayed on screen
* Solenoids aren't always turned off at the end of a song
* 

  

# Bugs / Needed Improvements

* The same video played 3 times in a row?
  * Once video is done playing, make sure it stops!
* Make sure the software actually pauses the hardware after the video is done playing for the specified time (e.g. 30 seconds)
* 
* Ensure data transmission between Arduino and PC is reliable (https://github.com/beneater/error-detection-videos)
* The load and save queues features need to be repaired
* [DONE] Next up only refreshes at weird times
* [DONE] the first element begins with 2.
* Change keys because they've all been leaked.
  * Proxy keys
  * berthatwo oauth
* Create a start message for visuals process
* If visuals.py can't connect to OBS after some time, the program will crash entirely.
  * What should the desired behaviour here be? If it can't connect, should it just wait until it can connect?
* Enable a GitHub action that cleans up python code?