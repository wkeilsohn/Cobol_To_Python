# William Keilsohn
# June 3 2025

# Import Packages
import os
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

# Testing Only
from time import sleep

# Declare Variables
cpath = os.getcwd()
pos_ans = 'YES'
cobol_text = ''
cobol_commands = pd.DataFrame()

# Define Functions

def checkUser(user_answer):
    global pos_ans
    if user_answer.upper() in pos_ans:
        return True
    else:
        return False

def getFileFromUser(): # Not used as for convience. Can be turned on at the user's discression. 
    file_name = input("What is the name of your cobol file?: ")
    if file_name[-3:] == 'cob':
        return file_name
    else:
        return (file_name + '.cob')

def findCobFile(): # Used to make testing fast. Can be toggled on and off.
    global cpath
    for root, dirs, files in os.walk(cpath):
        for i in files:
            if i[-3:] == "cob":
                return os.path.join(cpath, i)
    
def read_cobol_file(in_file):
    global cobol_text
    with open(in_file) as f:
        cobol_text = f.read()

def parseCobol():
    global cobol_text
    cobol_list = cobol_text.split('.')
    return cobol_list

def getProgramName():
    global cobol_commands


# Execute Program

if __name__ == "__main__":
    in_file = findCobFile() # Optional. Can be toggled with the line below. 
    # in_file = getFileFromUser() # Optional. Turned off for testing.
    read_cobol_file(in_file=in_file)
    cobol_list = parseCobol()
    out_name = in_file[:-4]
    out_file_name = "{}.py".format(out_name) # Change to program_id
    out_file = os.path.join(cpath, out_file_name)
    with open(out_file, "w") as f:
        for i in cobol_list:
            f.write(i)