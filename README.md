# Bertha2

Bertha2 is a hardware device that uses linear actuators to play the piano. It's essentially an external player piano.
We're able to do this using a microcontroller, 50 linear solenoids, solenoid control boards (essentially 2 transistors)
and a 500W power supply. Here's a video that shows the device in action:

[![Bertha2 plays "The Entertainer"](http://img.youtube.com/vi/F5GEH_fH9CI/0.jpg)](https://www.youtube.com/shorts/F5GEH_fH9CI)

On top of the hardware platform, we've built an integration with Twitch.tv. The idea is that we can livestream the device,
and viewers can control what is being played. Viewers submit links to YouTube videos via Twitch chat and the audio from the
video is converted to a MIDI file which is then played on the piano.


## More Footage

### Plants vs. Zombies

[![Video](http://img.youtube.com/vi/zee0DOZKW70/0.jpg)](https://youtube.com/shorts/zee0DOZKW70)

### Take 5

[![Video](http://img.youtube.com/vi/vYvGbFORp4I/0.jpg)](https://youtube.com/shorts/vYvGbFORp4I)


## Configuring

* Ensure the latest firmware is loaded onto the Arduino
* Install Ffmpeg using `brew install ffmpeg`
* Ensure al dependencies are installed and up to date. Reference `requirements.txt` for more information.
* Install the latest version of pytube by using `git clone git://github.com/nficano/pytube.git`. Anything else than the latest version will likely cause errors.



