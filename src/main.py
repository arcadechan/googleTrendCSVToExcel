import os
from time import sleep
from functions import prompt, run

cwd = os.getcwd()

if prompt(cwd):
    run(cwd)

sleep(5)
quit()