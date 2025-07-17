import sqlite3
import pandas as pd
import os
import shutil
from datetime import datetime,time
import time as t
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

import keyring
import Shira
from Shira import Newest_file


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver_service = Service(r"J:\Admin & Plans Unit\Recovery Systems\1. Systems\ChromeDriver\chromedriver.exe")
driver = webdriver.Chrome(service=driver_service, options=options)
wait = WebDriverWait(driver, 120)


FLPA_GP_username=keyring.get_password("FLPA_GP", "username")
FLPA_password=keyring.get_password("FLPA", "FLPA_password")

def FLPA_Login():

    driver.get("https://floridapa.org/")
    t.sleep(8)

    #Login to FLPA
    username_field=driver.find_element(By.NAME,"Username")
    password_field=driver.find_element(By.NAME,"Password")
    signIn_button=driver.find_element(By.NAME,"Submit")
    username_field.clear()
    password_field.clear()
    username_field.send_keys(FLPA_GP_username)
    password_field.send_keys(FLPA_password)
    signIn_button.click()
    t.sleep(5)




first = "test"
last = "user"
email = "test.user@example.com"
phone = "123-456-7890"
title = "test title"

def Add_user(First,Last,title,email,phone,role):
    FLPA_Login()
    driver.get(r"https://floridapa.org/app/#0?type=Contact")
    t.sleep(5)
    first_name_field = driver.find_element(By.ID, "NameFirst")
    last_name_field = driver.find_element(By.ID, "NameLast")
    title_field = driver.find_element(By.ID, "Title")
    email_field = driver.find_element(By.ID, "Email")
    phone_field = driver.find_element(By.ID, "PhoneBusiness")

    # value 1 is yes
    is_user_field = driver.find_element(By.XPATH, '//*[@id="IsUser"]')

# 2 is yes with restrictions 1 is yes unrestricted 0 is no
    has_assignments = driver.find_element(By.ID, "HasAssignments")


    # each group has an ID, need to find the correct one for the role
    # 1 = admin and 135 - applicant full/admin 103 applicant read only 102 applicant full
    role_field = driver.find_element(By.XPATH, '//*[@id="GroupIDs"]')


    first_name_field.click()
    first_name_field.send_keys(First)
    last_name_field.click()
    last_name_field.send_keys(Last)
    title_field.click()
    title_field.send_keys(title)
    email_field.click()
    email_field.send_keys(email)
    phone_field.click()
    phone_field.send_keys(phone)


    select_isuser = Select(is_user_field)
    t.sleep(2)
    select_isuser.select_by_value("1")
    t.sleep(2)
    select_assignments = Select(has_assignments)
    t.sleep(2)
    select_assignments.select_by_value("2")
    t.sleep(2)
    select_role = Select(role_field)
    t.sleep(2)
    select_role.select_by_visible_text("Applicant / Applicant Full Access")


Add_user(first,last,title,email,phone,"1")