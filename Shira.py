    
import keyring
import pandas as pd
from datetime import date, datetime, timedelta
import win32com.client
import time
import requests
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException 
from selenium.common.exceptions import TimeoutException
from zipfile import ZipFile
import shutil
import keyring
from datetime import date, datetime, timedelta
import win32com.client
import os
import re
import pandas as pd

# def main():



def refresh_excel(file):
    # replace file with file path
    filename=file
    xl = win32com.client.DispatchEx("Excel.Application")
    wb = xl.Workbooks.Open(filename)
    xl.Visible = True
    xl.DisplayAlerts = False
    time.sleep(60)
    wb.RefreshAll()
    time.sleep(60)
    xl.CalculateUntilAsyncQueriesDone()
    time.sleep(60)
    wb.Save()
    wb.Close(True)
    xl.Quit()
    print("Refresh Complete")  

# Sends webex message to the Recovery Data Team WEBEX chat (No notifications).
def webex_bot(message,file_path=None):

    def send_webex_message(access_token, room_id, message,file_path=None):
        url = f"https://webexapis.com/v1/messages"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            }
        # files = {"files":[file_path]}

        payload = {
            "roomId": room_id,
            "text": message,
        }

        if file_path is not None:
            payload["files"] = [file_path]


        response = requests.post(url, headers=headers, json=payload)
        print(response)
        if response.status_code == 200:
            print("Message sent successfully")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")
            print(response.text)

    access_token = "MGFjODlhZjQtM2RmOC00ZGJjLTg4ZjktOTc4NGEzMTk3YzE0YWM0NjZlODgtYmZk_PF84_f03967ef-dbf7-4f76-b680-a16d21ae48fb"
    room_id = "Y2lzY29zcGFyazovL3VzL1JPT00vZjdkMDllNTAtYzAzOC0xMWVlLWE3NDctNmIxM2YwZThhYWEw"
    message = (message)            
    file_path=(file_path)
    send_webex_message(access_token, room_id, message,file_path)




# Notification to the Script Detail WEBEX chat (notifications on).
def Webex_Alarm(message,file_path=None):
    def send_Alarm(access_token, room_id, message,file_path=None):
        url = f"https://webexapis.com/v1/messages"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            }
        # files = {"files":[file_path]}

        payload = {
            "roomId": room_id,
            "text": message,
        }

        if file_path is not None:
            payload["files"] = [file_path]


        response = requests.post(url, headers=headers, json=payload)
        print(response)
        if response.status_code == 200:
            print("Message sent successfully")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")
            print(response.text)

    access_token = "MGFjODlhZjQtM2RmOC00ZGJjLTg4ZjktOTc4NGEzMTk3YzE0YWM0NjZlODgtYmZk_PF84_f03967ef-dbf7-4f76-b680-a16d21ae48fb"
    room_id = "Y2lzY29zcGFyazovL3VzL1JPT00vM2VmZmI4ZTAtZTJkMi0xMWVlLThkNzEtNWJlZWFmZDVkN2E3"
    message = (message)            
    file_path=(file_path)
    send_Alarm(access_token, room_id, message,file_path)



def DB_Report_Notification(message, file_path=None):

    def send_webex_message(access_token, room_id, message, file_path=None):
        url = "https://webexapis.com/v1/messages"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        if file_path and os.path.isfile(file_path):
            # Send with attachment (multipart/form-data)
            with open(file_path, 'rb') as f:
                files = {'files': (os.path.basename(file_path), f)}
                data = {
                    "roomId": room_id,
                    "text": message
                }
                response = requests.post(url, headers=headers, data=data, files=files)
        else:
            # Send plain message (application/json)
            headers["Content-Type"] = "application/json"
            payload = {
                "roomId": room_id,
                "text": message
            }
            response = requests.post(url, headers=headers, json=payload)

        print(response)
        if response.status_code == 200:
            # print("Message sent successfully")
            pass
        else:
            print("logging system error")
            # print(f"Failed to send message. Status code: {response.status_code}")
            # print(response.text)

    access_token = "MGFjODlhZjQtM2RmOC00ZGJjLTg4ZjktOTc4NGEzMTk3YzE0YWM0NjZlODgtYmZk_PF84_f03967ef-dbf7-4f76-b680-a16d21ae48fb"
    room_id = "Y2lzY29zcGFyazovL3VzL1JPT00vY2FhMjA0NzAtNTA0MC0xMWYwLTk1MWMtMmI4YTYyNWQyOTk3"
    message = (message)            
    file_path=(file_path)
    send_webex_message(access_token, room_id, message,file_path)











# .... logs into grants portal, just give it a driver. (you must also have a current keyring and recieve the confirm email.)
def GP_Login(driver):
    FLPA_GP_username=keyring.get_password("FLPA_GP", "username")
    GP_password=keyring.get_password("GP", "GP_Password")
    def Raos_click_wait_id(elementid):
        # print("waiting for element "+ elementid +" to be clickable")
        delay = 10 #seconds
        waitloop = 1
        total_wait_time = delay
        while True:
            try:
                WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.ID, elementid)))
                # print ("Page is ready on try # " + str(waitloop))
                break # it will break from the loop once the specific element will be present. 
            except TimeoutException:
                waitloop = waitloop + 1
                total_wait_time = total_wait_time + delay
                if waitloop <= 5:
                    print ("Wait time total = " + str(total_wait_time) + " seconds. Trying again")
                else:
                    # print("Refreshing Page after " + str(waitloop) + " tries.")
                    waitloop = 1
                    driver.refresh()

    def Raos_locate_wait_class(elementclass):
        # print("waiting for element "+ elementclass +" to be clickable")
        delay = 10 #seconds
        waitloop = 1
        while True:
            try:
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, elementclass)))
                # print ("Page is ready on try # " + str(waitloop))
                break # it will break from the loop once the specific element will be present. 
            except TimeoutException:
                waitloop = waitloop + 1
                total_wait_time = waitloop * delay
                if waitloop <= 5:
                    print ("Wait time total = " + str(total_wait_time) + " seconds. Trying again")
                else:
                    # print("Refreshing Page after " + str(waitloop) + " tries.")
                    waitloop = 1
                    driver.refresh()
                # print ("Wait time total = " + str(total_wait_time) + " seconds. Trying again")


    #Part 2: Retreive passcode from email for authentication
    def retreive_passcode(delay, waitloop):
        print("Waiting for 2 Factor Authentication email to arrive")
        outlook = win32com.client.Dispatch('outlook.application')
        mapi = outlook.GetNamespace("MAPI")
        inbox = mapi.GetDefaultFolder(6)
        deleted_folder = mapi.GetDefaultFolder(3)  # Folder 3 is the Deleted Items folder
        received_dt = datetime.now() - timedelta(minutes=5)
        received_dt = received_dt.strftime('%m/%d/%Y %H:%M %p')
        delay = delay #seconds
        waitloop = waitloop
        passcodefound = 0
        print("waiting for " + str(delay)+ " seconds.")
        time.sleep(delay)
        messages = inbox.Items
        messages = messages.Restrict("[ReceivedTime] >= '" + received_dt + "'")
        messages = messages.Restrict("[SenderEmailAddress] = 'support.pagrants@fema.dhs.gov'")
        messages = messages.Restrict("[Subject] = 'Grants Portal Request'")
        print("filtered inbox, " + str(len(messages))+" found.")
        if len(messages) == 1:
            for message in messages:
                text=message.Body
                CodeRegexVariable=re.compile(r'(\d\d\d\d\d\d)')
                code=CodeRegexVariable.search(str(text))
                answer=code.group()
                print(answer)
                print("2 Factor Authentication email found and processed.")
                passcodefound = 1
                passcode_field=driver.find_element(By.ID,"passcode")
                passcode_field.clear()
                passcode_field.send_keys(answer)
                submit_button=driver.find_element(By.ID,"otpSubmitButton")
                submit_button.click()
                message.Move(deleted_folder)
                break
        else:
            waitloop = waitloop+1
            total_wait_time = waitloop * delay
            print ("Authentication email not found. Wait time total = " + str(total_wait_time) + " seconds. Waiting for "+str(delay)+" seconds and trying again")
            retreive_passcode(delay, waitloop)



    driver.get("https://grantee.fema.gov/")
    Raos_click_wait_id("username")
    username_field=driver.find_element(By.ID,"username")
    password_field=driver.find_element(By.ID,"password")
    signIn_button=driver.find_element(By.ID,"credentialsLoginButton")
    username_field.clear()
    password_field.clear()
    username_field.send_keys(FLPA_GP_username)
    password_field.send_keys(GP_password)
    signIn_button.click()
    time.sleep(15)
    accept_button=driver.find_element(By.CSS_SELECTOR,"button.btn.btn-sm.btn-primary")
    accept_button.click()
    time.sleep(10)
    accept_button2=driver.find_element(By.CSS_SELECTOR,"button.btn.btn-sm.btn-primary")
    time.sleep(10)
    accept_button2.click()
    time.sleep(10)
    
    retreive_passcode(30, 1)
    Raos_click_wait_id("quick-actions-btn")

# this will find the newest file in a folder, great for getting new dataframes with read_csv(Shira.Newest_File(folder_name)). 
def Newest_file(Folder_path):
    fileNames = []

    for file in os.listdir(Folder_path):
        # Ignore .db files (like Thumbs.db)
        if not file.lower().endswith('.db'):
            fileNames.append(file)

    # Sort files in reverse order to get the newest one first
    sorted_file_names = sorted(fileNames, reverse=True)

    # Check if the list is not empty to avoid index errors
    if sorted_file_names:
        return os.path.join(Folder_path, sorted_file_names[0])
    else:
        return None

# This clears ALL files in a folder and replaces it with the source_file
def Replace_File(source_file, destination):
    files = os.listdir(destination)
    if files:
        # If there are files, delete them
        for file in files:
            file_path = os.path.join(destination, file)
            os.remove(file_path)
        print("Deleted existing files in the folder.")

    # Copy the source file to the destination folder
    shutil.copy(source_file, destination)
    print(f"Copied {source_file} to {destination}.")

def df_to_csv_replace(dataframe, destination,name):
    files = os.listdir(destination)
    if files:
        # If there are files, delete them
        for file in files:
            file_path = os.path.join(destination, file)
            os.remove(file_path)
        print("Deleted existing files in the folder.")

    # Copy the source file to the destination folder
    dataframe.to_csv(rf"{destination}\{name}.csv", index= False)
    print(f"{name} saved to {destination}.")

# this will remove EVERYTHING in a folder
def clear_folder(folder_path):
# Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        # Check if the path is a file (not a directory)
        if os.path.isfile(file_path):
            # Delete the file
            os.remove(file_path)


#  this function will take the driver and close all tabs until 1 tab is left
def Clean_driver(driver):

    tabs = driver.window_handles
    
    if len(tabs) > 1:
        for tab in tabs[1:]:
            driver.switch_to.window(tab)
            driver.close()
        
        # Switch back to the first tab
        driver.switch_to.window(tabs[0])
        print("Closed all extra tabs. Only one tab is now open.")
    else:
        print("Only one tab is open.")

# this will allow the user to pass in multiple dataframes or a list of dataframes to append them together
def append_dfs(*args: pd.DataFrame | list[pd.DataFrame]) -> pd.DataFrame:
    if not args:
        raise ValueError("At least one DataFrame must be provided")
    elif len(args) == 1 and isinstance(args[0], list):
        dataframes = args[0]
        result = pd.concat(dataframes, ignore_index=True)
    else:
        dataframes = args
        result = pd.concat(dataframes, ignore_index=True)

    return result

def append_dfs_by_folder(folder):
    list = []
    for file in folder:
        dataframe = pd.read_csv(file)
        list.append(dataframe)
    large_dataframe = append_dfs(list)
    return large_dataframe
    

def save_csv_as_excel(csv_file_path, new_excel_path):
    import win32com.client as win32
    import os
    import time as t
    # Create an instance of Excel
    excel = win32.Dispatch('Excel.Application')
    t.sleep(3)
    excel.Visible = True 

    # Open the CSV file
    try:
        workbook = excel.Workbooks.Open(csv_file_path)

        # Save as Excel file in the specified new location
        workbook.SaveAs(new_excel_path, FileFormat=51)  # FileFormat=51 is for .xlsx

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if workbook:
            workbook.Close(SaveChanges=False)

        # If no other workbooks are open, quit the Excel application
        if excel.Workbooks.Count == 0:
            excel.Quit()


# if __name__ == '__main__':
#     main()
