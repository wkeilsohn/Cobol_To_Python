# William Keilsohn
# June 3 2025

# Import Packages
import os
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re

# Testing Only
from time import sleep

# Declare Variables
cpath = os.getcwd()
pos_ans = 'YES'
cobol_text = ''
cobol_ls = [] # Maybe? 
program_id = ''
working_storage_section = ''
procedure_division = ''


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
    global cobol_ls
    cobol_ls = cobol_text.split('.')

def cleanCobolLs():
    global cobol_ls
    cobol_ls = [x.lstrip() for x in cobol_ls]
    cobol_ls = list(filter(None, cobol_ls))

def getProgramName():
    global cobol_ls
    global program_id
    for i in cobol_ls:
        if i == 'PROGRAM-ID':
            j = cobol_ls.index(i) + 1
            program_id = cobol_ls[j]

def getWS():
    global cobol_text
    global cobol_ls
    global working_storage_section
    tmp_txt = ''
    for i in cobol_ls:
        tmp_txt = tmp_txt + i
    cobol_text = tmp_txt
    working_storage_section = re.findall(r'WORKING-STORAGE SECTION(.*?)PROCEDURE DIVISION', cobol_text)[0]

def getPD():
    global cobol_text
    global procedure_division
    procedure_division = re.findall(r'PROCEDURE DIVISION(.*?)STOP RUN', cobol_text)[0]

# Execute Program

if __name__ == "__main__":
    in_file = findCobFile() # Optional. Can be toggled with the line below. 
    # in_file = getFileFromUser() # Optional. Turned off for testing.
    read_cobol_file(in_file=in_file)
    parseCobol() # I can probably combine these functions... 
    cleanCobolLs()
    getProgramName()
    getWS()
    getPD()
    out_file_name = "{}.py".format(program_id)
    out_file = os.path.join(cpath, out_file_name)
    with open(out_file, "w") as f:
        for i in cobol_ls:
            f.write(i)