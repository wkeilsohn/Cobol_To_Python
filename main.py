# William Keilsohn
# June 3 2025

# Import Packages
import os
from bs4 import BeautifulSoup
import numpy as np

# Testing Only
from time import sleep

# Declare Variables
cpath = os.getcwd()
out_file = os.path.join(cpath, "cobol_file.py")
pos_ans = 'YES'
cobol_text = ''

# Define Functions

def checkUser(user_answer):
    global pos_ans
    if user_answer.upper() in pos_ans:
        return True
    else:
        return False

def getFileFromUser():
    file_name = input("What is the name of your cobol file?: ")
    if file_name[-3:] == 'cob':
        return file_name
    else:
        return (file_name + '.cob')
    
def read_cobol_file(in_file):
    global cobol_text
    with open(in_file) as f:
        cobol_text = f.read()

# Execute Program

if __name__ == "__main__":
    in_file = getFileFromUser()
    read_cobol_file(in_file=in_file)
    print(cobol_text)
    sleep(25) # Testing only. Remove later.