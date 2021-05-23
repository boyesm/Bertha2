import subprocess

subprocess.run("python3 converter.py & python3 twitch_request_handler.py", shell=True)