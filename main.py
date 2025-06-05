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
        var_name = re.search(r' (.*?)PIC', ws_value)[0][:-3]
        var_name = var_name.lstrip()
        var_value = re.search(r'(?<= VALUE).+', ws_value)
        if var_value is None:
            var_value = 0
        elif var_value[0] == 'VALUE':
            var_value = 0
        elif "ZERO" in var_value[0]:
            var_value = 0
        else:
            var_value = var_value[0]
        tmp_str = str(var_name) + '= ' + str(var_value)
    return tmp_str 

# def buildPD(func_core, function_name): # Add Later. This is a good idea, but not yet needed.
#     header = "def "

def buildCMD(cmd_core):
    cmd_value = ""
    if 'MOVE' in cmd_core:
        cn_value = re.findall(r'\d+', cmd_core)[0]
        cv_value = re.search(r'(?<= TO ).+', cmd_core)[0]
        cmd_value = str(cv_value) + " = " + str(cn_value)
    elif 'DISPLAY' in cmd_core:
        cv_value = re.search(r'(?<=DISPLAY ).+', cmd_core)[0]
        cmd_value = "print(" + str(cv_value) + ")" 
    elif 'STRING' in cmd_core:
        c1_value = re.findall(r'STRING (.*?) DELIMITED', cmd_core)[0]
        if 'SPACE' in cmd_core:
            cm_value = '" "'
            c2_value = re.findall(r'SPACE (.*?) DELIMITED', cmd_core)[0].lstrip()
        else:
            cm_value = ''
            c2_value = re.findall(r'SIZE(.*?) DELIMITED', cmd_core)[0]
        c3_value = re.search(r'(?<=INTO ).+', cmd_core)[0].lstrip()
        cmd_value = str(c3_value) + '=' + str(c1_value)\
            + "+" + str(cm_value)+ "+" + c2_value # Can and should be expanded upon. 
    elif 'COMPUTE' in cmd_core:
        cmd_core = cmd_core.replace("EQUALS", "=")
        eq_value = re.search(r'(?<=\=).+', cmd_core)[0]
        cv_value = re.findall(r'COMPUTE (.*?) \=', cmd_core)[0]
        cmd_value = str(cv_value) + " = " + eq_value
    else:
        pass # A lot more to expand upon...
    return cmd_value

def getWS():
    global cobol_text
    global working_storage_section
    tmp_txt = " ".join(cobol_text.split('\n'))
    working_storage_section = re.findall(r'WORKING-STORAGE SECTION\.(.*?)PROCEDURE DIVISION\.', tmp_txt)[0]



def getPD():
    global cobol_text
    global procedure_division
    tmp_txt = " ".join(cobol_text.split('\n'))
    procedure_division = re.findall(r'PROCEDURE DIVISION\.(.*?)STOP RUN\.', tmp_txt)[0]


def startFile(run_file_name, start_value=False):
    if start_value == True:
        os.system("python {}".format(run_file_name))

def wsToVariables():
    global working_storage_section
    tmp_vals = ''
    working_storage_section_ls = working_storage_section.split('.')
    for i in working_storage_section_ls:
        tmp_vals = tmp_vals + '\n' + assignWSS(i)
    working_storage_section = tmp_vals

def pdTofunctions():
    global procedure_division
    tmp_vals = []
    pd_ls = procedure_division.split('.')
    for i in pd_ls:
        tmp_vals.append(buildCMD(i))
    procedure_division = tmp_vals

def createRunCommand():
    global procedure_division
    run_command = ""
    spacer = "    "
    run_command = run_command + 'if __name__ == "__main__":'
    for i in procedure_division:
        run_command = run_command + "\n" + spacer + i
    return run_command

# Execute Program

if __name__ == "__main__":
    in_file = findCobFile() # Optional. Can be toggled with the line below. 
    # in_file = getFileFromUser() # Optional. Turned off for testing.
    read_cobol_file(in_file=in_file)
    cleanCobolLs()
    getProgramName()
    getWS()
    wsToVariables()
    getPD()
    pdTofunctions()
    start_func = createRunCommand()
    out_file_name = "{}.py".format(program_id)
    out_file = os.path.join(cpath, out_file_name)
    with open(out_file, "w") as f:
        f.write(working_storage_section)
        f.write("\n")
        f.write(start_func)
    startFile(run_file_name=out_file) # Toggle On / Off