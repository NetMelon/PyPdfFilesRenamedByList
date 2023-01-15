#!/usr/bin/env python3

"""
Renames all PDF files in the direcory of this script if search terms of "data.json" file apply according to a configurable style 

Run once and see how the name of "test-file.pdf" is changed.

"""

# IMPORTS

import json
import glob
import os
import pypdf
import datetime



# CONFIG

# Should the current date be set in the beginning of the filename?
currentDateInFilenameAtBeginning = True

# Write any string here that should be added to the end of each filename
SpecialStringInFilenameAtEnd = "abc"

# Opening JSON file
with open('data.json', encoding='utf-8') as json_file:
    data = json.load(json_file)
rename_table = data["root"]



# FUNCTIONS

# Function: Find any of the Strings in the list and mark Boolean for "Found" or "Not Found"
def checkSearchTermOccurance(string_list):
    bool_list = []
    for i in range(len(string_list)):
            string = string_list[i]
            bool_list.append(checkSubstringExists(content, string))
    return all(item is True for item in bool_list)

# Function to extract number of pages in the document
def checkSubstringExists(fullstring, substring):
    if substring in fullstring:
        return True
    else:
        return False

# Function: Get the current date
def currentDate(boolean):
    if(boolean == True):
        return datetime.date.today().strftime('%Y-%m-%d')
    else:
        return ""

# Function to return the number of pages from a PDF document
def getNumPages(path):
    with open(path, "rb") as p:
        pdf = pypdf.PdfReader(p)
        return len(pdf.pages)

# Function to extract content from PDF document
def getPDFContent(path, num_pages):
    content = ""
    with open(path, "rb") as p:
        pdf = pypdf.PdfReader(p)
        for i in range(0, num_pages):
            content += pdf.pages[i].extract_text() + "\n"
            content = " ".join(content.replace(u"\xa0", " ").strip().split())
    return content



# CODE

# Scanning for all PDF-files in current directory and creating a list with the paths to the files
path = (os.getcwd()+'\*.pdf')
pathsList = glob.glob(path)

# Using for loop on the PDF-files in the directory
for path in pathsList:
    number_pages = getNumPages(path)
    # Extracting the content from PDF-files
    content = getPDFContent(path, number_pages)
    print(path)
    # For each dataset in the data table with potential renames ...
    for k in range(len(rename_table)):
        if checkSearchTermOccurance(rename_table[k]["searchTerms"]) == True:
            filename = str(currentDate(currentDateInFilenameAtBeginning) 
                           + "_" 
                           + rename_table[k]["rename_addInfo"] 
                           + "_" 
                           + rename_table[k]["rename_lastname"] 
                           + ( "_" 
                           + rename_table[k]["rename_firstname"] if rename_table[k]["rename_firstname"] else "")
                           + ("_"
                           + SpecialStringInFilenameAtEnd if SpecialStringInFilenameAtEnd else ""))
            print(filename)
            print(os.getcwd() + "\\" + filename + ".pdf")
            try:
                os.rename(path, os.getcwd() + "\\" + filename + ".pdf")
            except FileExistsError:
                print("File already Exists")
                print("Removing existing file")
                # skip the below code, if you don't' want to forcefully rename
                os.remove(path, os.getcwd() + "\\" + filename + ".pdf")
                # rename it
                os.rename(path, os.getcwd() + "\\" + filename + ".pdf")
                print('Done renaming a file')
            # break the inner loop
            break
        else:
            # will be called if the previous loop did not end with a `break` 
            continue