#!/usr/bin/env python
# coding: utf-8

# # Hacker Challenge 2020
# Write a 🐍 program that logs on the Hub and downloads module files.

# ## Imports

# In[ ]:


import subprocess
import sys
import os
from zipfile import ZipFile
import easygui as eg
from selenium import webdriver
from selenium.webdriver.common.keys import Keys # Keys in the keyboard
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from sys import platform

def install(package):
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])


# ## User Inputs

# In[ ]:


user_username = input("Insert Username (e.g. af2230):    ") # Get username
user_password = input("Insert Password:    ") # Get password
        
# Install the required packages (Specified in the requirements.txt file)
with open("requirements.txt") as f:
    for pk in f:
        install(pk)


# Specify donwnload folder --> The files will be downloaded and unzipped in a folder called "Courses_Downloads" that will be created where is script is located
download_folder_path = os.getcwd()
download_folder_path = os.path.join(download_folder_path,"Courses_Downloads")


# Parameters for the GUI
question = "What courses do you want to download?  The files will be downloaded in a folder called  'Courses_Downloads' stored in the same folder where this script is stored"
title = "Select courses"
courses = ["Math", "FDT", "DSA"] # Avaiable courses


choice = eg.multchoicebox(question , title, courses) # pop-up of multiple choice questionaire
courses = choice


# ## Links to the modules file folder

# In[ ]:


# Paths to the course File folders
# These are the paths to the embedded dropbox Iframe
paths_to_file = {"Math": "https://www.dropbox.com/dropins/embed?app_key=61vxbrvh0awtwwr&origin=https%3A%2F%2Fiframed.insendi.com&link=https%3A%2F%2Fwww.dropbox.com%2Fsh%2Ft14inxc5bfcwaqu%2FAADiq3JtxF07oJ3ymOe94nH2a%3Fdl%3D0&iframe=false",
                 "FDT":"https://www.dropbox.com/dropins/embed?app_key=61vxbrvh0awtwwr&origin=https%3A%2F%2Fiframed.insendi.com&link=https%3A%2F%2Fwww.dropbox.com%2Fsh%2F7w7a76i95jtl3ca%2FAADl7D_Tn6xUZ97KCdzmxl-sa%3Fdl%3D0&iframe=false",
                 "DSA":"https://www.dropbox.com/dropins/embed?app_key=61vxbrvh0awtwwr&origin=https%3A%2F%2Fiframed.insendi.com&link=https%3A%2F%2Fwww.dropbox.com%2Fsh%2Fwji42tbpgzpfzir%2FAADnJYBolgVuVDYvJ4nI2wQla%3Fdl%3D0&iframe=false"}


# ### Opening a Chrome Browser

# In[ ]:


# Checking what platform is being used so to make sure that we are using the right version of chome (I used the chrome 85 webdriver)
if platform == "linux" or platform == "linux2":
    pass
if platform == "darwin":
    chromedriver = os.getcwd()
    chromedriver = os.path.join(chromedriver,"chromedriver") # Mac
if platform == "win32":
    chromedriver = os.getcwd()
    chromedriver = os.path.join(chromedriver,"win_chromedriver.exe") # Windows



chrome_options = Options() 

# Turn off chrome warning for multiple downloads
prefs = {'profile.default_content_setting_values.automatic_downloads': 1,"download.default_directory" : download_folder_path}
chrome_options.add_experimental_option("prefs", prefs)


driver = webdriver.Chrome(chromedriver,options=chrome_options) # Opening the chrome browser


# ### Connecting to the Hub trough the Imperial Login 

# In[ ]:


# Connecting to the login form
driver.get('https://imperial.insendi.com/auth/saml/authenticate/imp?returnPath=/')


# ### Entering the Username and Password

# In[ ]:


elem_username = driver.find_element_by_name("j_username") # find the login text-box
elem_username.clear() # Clear text in the login text-box
elem_username.send_keys(user_username) # Typing the username into the login textbox

elem_password = driver.find_element_by_name("j_password")
elem_password.clear()
elem_password.send_keys(user_password)


elem_password.send_keys(Keys.RETURN) # Hitting the return key


# ### Connecting to the Dropbox folder and downloading the files

# In[ ]:


# For each course specified by the user:

for course in courses:
    dropdox_Path = paths_to_file[course] # Get the path to the dropbox iframe (Specified in the paths_to_file dictionary)
    driver.get(dropdox_Path) # Connect to the dropbox iframe for that course
    time.sleep(3) # Wait 3 seconds so that it loads
    driver.find_element_by_xpath("//button[@aria-label='Download']").click() # find and click the download button
    time.sleep(3) # Wait 3 seconds before going to the next step


# ### Wait untill the downloads are finished

# In[ ]:


# Waits and checks every second to see if the dowloads are completed

seconds = 0
wait = True
while wait:
    time.sleep(1)
    wait = False
    for fname in os.listdir(download_folder_path):
        if fname.endswith('.crdownload'): # If there is still a file with the .crdownload extension this means that the download is still not complete.
            wait = True
    seconds += 1
    if seconds %5 ==0:
        print("Seconds passed since the start of the downloads ",seconds) # Prints how many seconds passed since the start of download


# ### Unzipping the downloaded folders and renaming them

# In[ ]:


downloads = os.listdir(download_folder_path)
downloads_zips = [i for i in downloads if ".zip" in i and "crd" not in i] # List of all the downloads names
zip_paths = [os.path.join(download_folder_path,i) for i in downloads_zips]
the_len = len(zip_paths[0])
if not all(len(l) == the_len for l in zip_paths): # Sorts the names in the order they were downlaoded (So that we can then rename the folders)
    zip_paths = sorted(zip_paths)
    zip_paths = zip_paths[-1:] + zip_paths[:-1] 
else:
    zip_paths = sorted(zip_paths)
    
    
    
for i,zip_fold in enumerate(zip_paths):
    with ZipFile(zip_fold, 'r') as zipObj:
       # Extract all the contents of zip file in current directory
       zipObj.extractall(os.path.join(download_folder_path,courses[i])) # Extracting the elements into the folders with the correspondant course name


# ### Removing the .zip files

# In[ ]:


for zip_path in zip_paths:
    os.remove(zip_path) # After extraction delete the zip files

