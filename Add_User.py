import sqlite3
import pandas as pd
import os
import shutil
from datetime import datetime, time
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

FLPA_GP_username = keyring.get_password("FLPA_GP", "username")
FLPA_password = keyring.get_password("FLPA", "FLPA_password")
processing_list = pd.DataFrame(columns=[
    "First Name", "Last Name", "Email", "Phone", "Title", "Has Assignments", "Roles"
])

def FLPA_Login():
    driver.get("https://floridapa.org/")
    t.sleep(8)
    username_field = driver.find_element(By.NAME, "Username")
    password_field = driver.find_element(By.NAME, "Password")
    signIn_button = driver.find_element(By.NAME, "Submit")
    username_field.clear()
    password_field.clear()
    username_field.send_keys(FLPA_GP_username)
    password_field.send_keys(FLPA_password)
    signIn_button.click()
    t.sleep(5)

AVAILABLE_ROLES = [
    "Applicant",
    "CIVIX Employee (System Administrator)",
    "CIVIX Employee (System Administrator) [Read-Only]",
    "Contractor",
    "External Auditor (Read-Only)",
    "State",
    "State Read-Only",
    "System Administrator",
    "System Administrator Backup",
    "Applicant / Applicant Full Access",
    "Applicant / Applicant Read-Only",
    "Applicant / Applicant Full Access / Applicant Admin",
    "State / Grant Program Manager / Lead Grant Program Manager",
    "State / Account Closeout",
    "State / Appeals",
    "State / DAC Payables",
    "State / Grant Manager",
    "State / Grant Program Manager",
    "State / Project Closeout",
    "State / Quality Assurance/ Quality Control Unit",
    "State / Receivables",
    "State / RPA Approver",
    "State / Small Project Closeout",
    "State / State Audit Tracking",
    "State / State Finance & Accounting",
    "State / State GAR",
    "State / State Legal",
    "State Read-Only / FEMA Closeout",
    "State Read-Only / FEMA PAC"
]

def append_user():
    global processing_list
    roles = [roles_listbox.get(i) for i in roles_listbox.curselection()]
    if not roles:
        messagebox.showerror("Error", "Select at least one role.")
        return
    new_row = {
        "First Name": entries["First Name"].get(),
        "Last Name": entries["Last Name"].get(),
        "Email": entries["Email"].get(),
        "Phone": entries["Phone"].get(),
        "Title": entries["Title"].get(),
        "Has Assignments": has_assignment_var.get(),
        "Roles": ", ".join(roles)
    }
    processing_list = processing_list.append(new_row, ignore_index=True)
    messagebox.showinfo("Success", "User data added to list.")
    clear_form()

def clear_form():
    for e in entries.values():
        e.delete(0, tk.END)
    has_assignment_var.set(2)
    roles_listbox.selection_clear(0, tk.END)


def Add_user(First, Last, title, email, phone, assignments, selected_roles):
    
    driver.get(r"https://floridapa.org/app/#0?type=Contact")
    t.sleep(2)
    driver.refresh()
    t.sleep(5)


    first_name_field = driver.find_element(By.ID, "NameFirst")
    last_name_field = driver.find_element(By.ID, "NameLast")
    title_field = driver.find_element(By.ID, "Title")
    email_field = driver.find_element(By.ID, "Email")
    phone_field = driver.find_element(By.ID, "PhoneBusiness")

    is_user_field = driver.find_element(By.XPATH, '//*[@id="IsUser"]')
    has_assignments = driver.find_element(By.ID, "HasAssignments")
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

    select_assignments = Select(has_assignments)
    t.sleep(2)
    select_assignments.select_by_value(assignments)

    select_role = Select(role_field)
    t.sleep(2)

    # Debug: show what's available
    print("Available roles in dropdown:")
    for option in select_role.options:
        print(f"- {option.text.strip()}")

    for r in selected_roles:
        try:
            select_role.select_by_visible_text(r)
        except:
            print(f"Role '{r}' not found in the dropdown")

def process_all_users():
    FLPA_Login()

    if processing_list.empty:
        messagebox.showerror("Error", "No users to process.")
        return
    for idx, row in processing_list.iterrows():
        role_list = [r.strip() for r in row["Roles"].split(",")]
        Add_user(
            row["First Name"],
            row["Last Name"],
            row["Title"],
            row["Email"],
            row["Phone"],
            str(row["Has Assignments"]),
            role_list
        )
    messagebox.showinfo("Success", "All users processed.")


root = tk.Tk()
root.title("Add User to FLPA")

entries = {}
fields = ["First Name", "Last Name", "Email", "Phone", "Title"]

for i, field in enumerate(fields):
    tk.Label(root, text=field).grid(row=i, column=0, sticky="w")
    entry = tk.Entry(root, width=40)
    entry.grid(row=i, column=1)
    entries[field] = entry


tk.Label(root, text="Has Assignments?").grid(row=5, column=0, sticky="w")
has_assignment_var = tk.IntVar(value=2)
tk.Radiobutton(root, text="Yes", variable=has_assignment_var, value=2).grid(row=len(fields), column=1, sticky="w")
tk.Radiobutton(root, text="No", variable=has_assignment_var, value=0).grid(row=len(fields), column=1, sticky="e")

tk.Label(root, text="Select Roles").grid(row=len(fields)+1, column=0, sticky="nw")
roles_listbox = tk.Listbox(root, selectmode="multiple", height=10, width=50)
roles_listbox.grid(row=len(fields)+1, column=1)
for role in AVAILABLE_ROLES:
    roles_listbox.insert(tk.END, role)

def on_submit():
    first = entries["First Name"].get()
    last = entries["Last Name"].get()
    email = entries["Email"].get()
    phone = entries["Phone"].get()
    title = entries["Title"].get()
    assignments = str(has_assignment_var.get())
    selected_indices = roles_listbox.curselection()
    selected_roles = [roles_listbox.get(i) for i in selected_indices]

    if not selected_roles:
        messagebox.showerror("Error", "Select at least one role.")
        return

    Add_user(first, last, title, email, phone, assignments, selected_roles)

append_btn = tk.Button(root, text="Add to List", command=append_user, bg="blue", fg="white")
append_btn.grid(row=len(fields)+3, column=0, pady=10)

process_btn = tk.Button(root, text="Process All", command=process_all_users, bg="green", fg="white")
process_btn.grid(row=len(fields)+3, column=1, pady=10)

root.mainloop()
