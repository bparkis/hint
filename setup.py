#!/usr/bin/python3
import os
import subprocess

def setupEnv():
    subprocess.run(["bash -c 'python3 -m venv .env && source .env/bin/activate && pip install -r requirements.txt'"], shell=True)

def setupBashrc():
    bashrcFile = os.path.expanduser(os.path.join("~", ".bashrc"))
    if not os.path.exists(bashrcFile):
        with open(bashrcFile, 'w') as f:
            pass
    with open(bashrcFile) as f:
        s = f.read()
        if "HINT_DIR=" in s:
            print("Your .bashrc looks like it's already set up for hint.")
            return
    answer = input("Set up your ~/.bashrc for hint? [y/n] ")
    if answer in 'yY':
        script_dir = os.path.dirname(os.path.realpath(__file__))
        with open(bashrcFile, 'a') as f:
            f.write("\n\nHINT_DIR=" + script_dir)
            f.write("\nsource $HINT_DIR/hint.sh")
            f.write("\n# export HINT_MENUS_DIR=" + os.path.join(script_dir, "menus") + "\n")

if __name__ == "__main__":
    setupEnv()
    setupBashrc()
