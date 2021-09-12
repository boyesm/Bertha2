#!/bin/bash

python init.py

python livestream.py &
python converter.py &
python twitch_request_handler.py &