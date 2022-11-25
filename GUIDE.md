# Development Guide

* macOS is assumed.
* After every change to OBS scenes, please export them and sync them with Git

## Before Using the Program

* Install `requirements.txt`
* Ensure FFmpeg is installed. Use `brew install ffmpeg` to install.
* Ensure TKinter is installed. Use `brew install python-tk` to install.
* Ensure `secrets.env` is present in the main directory. If it's not, create it and input the proper information.
* Import OBS scenes
* Open OBS


## Secrets.env File

This file should include Twitch auth information and OBS local password. It should be of the format:

```
TOKEN=oauth:
CLIENT_ID=
NICKNAME=berthatwo
OBSPSWD=
```

## Hardware Simulator

Start netcat in a new terminal before running the hardware tests. This will allow the outputs of the 
solenoids to be viewed on the command line.

```commandline
nc -dkl 8001
```


## Importing and Exporting OBS Scenes

* In the `/obs-media` directory, the OBS scenes that work with this program are saved.
* They can be imported into OBS by going to `Scene Collection > Import`
* After a scene has been modified, export it in OBS by going to `Scene Collection > Export`