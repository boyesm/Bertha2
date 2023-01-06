# Development Guide

* macOS is assumed.
* After every change to OBS scenes, please export them and sync them with Git

## Before Using the Program

* Install `requirements.txt`
* Ensure FFmpeg is installed. Use `brew install ffmpeg` to install.
* Ensure `secrets.env` is present in the main directory. If it's not, create it and input the proper information.
* Get OBS working
  * Install version 28.xx of OBS. This will be default include version 5+ of `obs-websockets`. Ensure version 1+ of `simpleobsws` is installed.
    * A verified combination of working services is OBS v28.xx, `obs-websockets` v5.x, and `simpleobsws` v1.x
  * Configure `obs-websockets`. Set server port to `4444` in the `obs-websocket` settings. There are some issues with the default port.
  * Import OBS scenes from the `obs-media` directory
  * Input the B2 stream key. This can be found in `secrets.env`.


## Setting Up Test Environment

* When testing without hardware, open new terminal and enter netcat command:
    `nc -dkl 8001`
* Open OBS, import presets
* Start streaming with B2 creds
* Run B2 software in test mode
* Run `test_stream.py` script


## Secrets.env File

This file should include Twitch auth information and OBS local password. It should be of the format:

#TODO: this isn't up to date.

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

## Using Pycharm

* To enable the coloured output in PyCharm (much nicer), enable "Emulate terminal in output console" in run configuration
* To enable this setting by default on all new run configurations:
  1. Go to RUN > EDIT CONFIGURATIONS
  2. Go to "Edit configuration templates..." at the bottom left of the new window
  3. Check the "Emulate terminal in output console" box and apply


