#!/bin/bash

python init.py

python livestream.py &
python converter.py &
python request_handler.py &