# v1.0 roadmap

* [DONE] Fix Saved Queue
  * Will the queue save videos even if it's in the process of shutting down?
* [DONE] Modify peak and hold voltage function
* Doesn't play the first video that's requested (on startup, or on restart)
* It currently plays image files (!play https://i.ytimg.com/vi/QNQQGO2WJbM/hqdefault.jpg?sqp=-oaymwE2CNACELwBSFXyq4qpAygIARUAAIhCGAFwAcABBvABAfgBvgSAAoAIigIMCAAQARhyIFooQDAP&rs=AOn4CLCaDbi7K59Dw3oIoKaZXVtCsKV8Nw)
* If a link that doesn't work gets past initial filter, make sure it doesn't fuck everything up.
* Make a message saying the bot is down when it closes (i.e. set obs text to something like "bot is offline for maintenaince")
* Why are other users seeing messages from berthatwo? All responses to !play commands should be whispers
* Add some serious try catches to this code so things don't go wrong
* Is this queueing every video?
* Add some better explanations for what is going on (why does your video not immediately appear in next up? why does the bot not respond to only "!play"?)

READ THIS: https://go.snyk.io/rs/677-THP-415/images/Python_Cheatsheet_whitepaper.pdf

# Some bigger things to implement

* Easy and consistent testing (even without hardware connected)
  * [DONE] Hardware simulator
  * [DONE] Documented test setup guide
  * [DONE] Write a script that stress tests the stream
* Better logging, some way of enabling different levels of information without constantly commenting out print statements
  * [DONE] Control general log level, when debugging, debug level logs should be enabled
  * [DONE] Also be able to control log level for each module, when troubleshooting a single module for example, all debug level logs are not needed
  * Make sure the log levels are accurate to what they are. Document how to level logs.
  * Change log level while program is running? https://towardsdatascience.com/how-to-add-a-debug-mode-for-your-python-logging-mid-run-3c7330dc199d
  * Save logs to files
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
* [DONE] The bot should respond to chat messages to let the user know their video has been queued

  

# Bugs / Needed Improvements

* Implement a better peak and hold system. Solenoids shouldn't get so hot all the time.
* Make sure all solenoids turn off once done. There are often still signals left on after everything is done playing.
* The load and save queues features need to be repaired
* [DONE] Make sure the software actually pauses the hardware after the video is done playing for the specified time (e.g. 30 seconds)
* [DONE] The same video played 3 times in a row?
* [DONE] Once video is done playing, make sure it stops!
* Ensure data transmission between Arduino and PC is reliable (https://github.com/beneater/error-detection-videos)
* [DONE] Next up only refreshes at weird times
* [DONE] the first element begins with 2.
* Change keys because they've all been leaked.
  * Proxy keys
  * berthatwo oauth
* Create a start message for visuals process
* If visuals.py can't connect to OBS after some time, the program will crash entirely.
  * What should the desired behaviour here be? If it can't connect, should it just wait until it can connect?
* Enable a GitHub action that cleans up python code?