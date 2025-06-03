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

# Execute Program

if __name__ == "__main__":
    in_file = getFileFromUser()
    print(in_file)
    sleep(5) # Testing only. Remove later.