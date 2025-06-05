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

# def parseCobol():
#     global cobol_text
#     global cobol_ls
#     cobol_ls = cobol_text.split('.')

def cleanCobolLs():
    global cobol_ls
    global cobol_text
    cobol_ls = cobol_text.split('.')
    cobol_ls = [x.lstrip() for x in cobol_ls]
    cobol_ls = list(filter(None, cobol_ls))

def getProgramName():
    global cobol_ls
    global program_id
    for i in cobol_ls:
        if i == 'PROGRAM-ID':
            j = cobol_ls.index(i) + 1
            program_id = cobol_ls[j]

def assignWSS(ws_value): # Expand upon later
    tmp_str = ""
    ws_value = ws_value.lstrip()
    if "PIC" not in ws_value:
        pass # Add Later
    else:
        var_name = re.search(r' (.*?)PIC', ws_value)[0][:-3] # There is probably a better way.
        var_value = re.search(r'VALUE(.*?)\.', ws_value)
        if var_value is None:
            var_value = 0
        elif len(var_value) == 0:
            var_value = 0
        elif var_value[0] in "ZEROS":
            var_value = 0
        else:
            var_value = var_value[0]
        tmp_str = str(var_name) + ' = ' + str(var_value)
    return tmp_str 


def getWS():
    global cobol_text
    global working_storage_section
    tmp_txt = " ".join(cobol_text.split('\n'))
    working_storage_section = re.findall(r'WORKING-STORAGE SECTION\.(.*?)PROCEDURE DIVISION\.', tmp_txt)[0]



def getPD():
    global cobol_text
    global procedure_division
    tmp_txt = " ".join(cobol_text.split('\n'))
    procedure_division = re.findall(r'PROCEDURE DIVISION(.*?)STOP RUN', tmp_txt)


def startFile(run_file_name, start_value=False):
    if start_value == True:
        os.system("python {}".format(run_file_name))


# def createRunCommand():

def wsToVariables():
    global working_storage_section
    tmp_vals = ''
    working_storage_section_ls = working_storage_section.split('.')
    for i in working_storage_section_ls:
        tmp_vals = tmp_vals + '\n' + assignWSS(i)
    working_storage_section = tmp_vals

# Execute Program

if __name__ == "__main__":
    in_file = findCobFile() # Optional. Can be toggled with the line below. 
    # in_file = getFileFromUser() # Optional. Turned off for testing.
    read_cobol_file(in_file=in_file)
    # parseCobol() # I can probably combine these functions... 
    cleanCobolLs()
    getProgramName()
    getWS()
    wsToVariables()
    getPD()
    out_file_name = "{}.py".format(program_id)
    out_file = os.path.join(cpath, out_file_name)
    with open(out_file, "w") as f:
        f.write(working_storage_section)
    startFile(run_file_name=out_file) # Toggle On / Off