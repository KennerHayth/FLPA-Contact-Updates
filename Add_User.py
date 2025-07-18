import sqlite3

import threading

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

Used_emails = pd.read_csv(Shira.Newest_file(r"J:\Admin & Plans Unit\Recovery Systems\2. Reports\4. Data Files\FLPA Contacts"))

Used_emails = Used_emails["Contact Email"].str.strip().str.lower().unique()
selected_index = [None] 
user_assignments = {}


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

def start_tkinter():
    root = tk.Tk()
    root.title("Add User to FLPA")
    root.attributes('-topmost', True)

    entries = {}
    fields = ["First Name", "Last Name", "Email", "Phone", "Title"]

    # Sidebar Listbox for users
    tk.Label(root, text="Users to be Added").grid(row=0, column=2, sticky="nw", pady=(0, 2))

    # Sidebar Listbox for users
    user_listbox = tk.Listbox(root, height=20, width=30)
    user_listbox.grid(row=1, column=2, rowspan=len(fields)+5, padx=(10,0), pady=(0,5), sticky="nw")

    def load_selected_user(event):
        selection = user_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        selected_index[0] = index
        row = processing_list.iloc[index]
        for field in fields:
            entries[field].delete(0, tk.END)
            entries[field].insert(0, row[field])
        has_assignment_var.set(int(row["Has Assignments"]))

        # Deselect and select matching roles
        roles_listbox.selection_clear(0, tk.END)
        role_names = [r.strip() for r in row["Roles"].split(",")]
        for i, role in enumerate(AVAILABLE_ROLES):
            if role in role_names:
                roles_listbox.selection_set(i)

    user_listbox.bind('<<ListboxSelect>>', load_selected_user)


    def append_user():
        global processing_list
        roles = [roles_listbox.get(i) for i in roles_listbox.curselection()]
        if not roles:
            messagebox.showerror("Error", "Select at least one role.")
            return
        email = entries["Email"].get().strip().lower()
        if email in Used_emails:
            messagebox.showwarning("Warning", f"The email '{email}' is already used. User not added.")
            return
        phone = entries["Phone"].get().strip()
        if phone.isdigit() and len(phone) >= 10:
            pass
        else:
            messagebox.showerror("Error", "Phone number must at least 10 digits.")
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
        # Add user to sidebar
        user_listbox.insert(tk.END, f"{new_row['First Name']} {new_row['Last Name']}")
        messagebox.showinfo("Success", "User data added to list.")
        clear_form()

    def update_user():
        if selected_index[0] is None:
            messagebox.showerror("Error", "No user selected for editing.")
            return

        roles = [roles_listbox.get(i) for i in roles_listbox.curselection()]
        if not roles:
            messagebox.showerror("Error", "Select at least one role.")
            return

        email = entries["Email"].get().strip().lower()
        if email in Used_emails and email != processing_list.iloc[selected_index[0]]["Email"]:
            messagebox.showwarning("Warning", f"The email '{email}' is already used. Cannot update.")
            return

        phone = entries["Phone"].get().strip()
        if not phone.isdigit() or len(phone) < 10:
            messagebox.showerror("Error", "Phone number must be at least 10 digits and numeric.")
            return

        new_data = {
            "First Name": entries["First Name"].get(),
            "Last Name": entries["Last Name"].get(),
            "Email": email,
            "Phone": phone,
            "Title": entries["Title"].get(),
            "Has Assignments": has_assignment_var.get(),
            "Roles": ", ".join(roles)
        }

        for key in new_data:
            processing_list.at[selected_index[0], key] = new_data[key]
        user_listbox.delete(selected_index[0])
        user_listbox.insert(selected_index[0], f"{new_data['First Name']} {new_data['Last Name']}")
        messagebox.showinfo("Updated", "User updated successfully.")
        clear_form()
        selected_index[0] = None


    def clear_form():
        for e in entries.values():
            e.delete(0, tk.END)
        has_assignment_var.set(2)
        roles_listbox.selection_clear(0, tk.END)

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
    roles_listbox = tk.Listbox(root, selectmode="extended", height=10, width=50)
    roles_listbox.grid(row=len(fields)+1, column=1)
    for role in AVAILABLE_ROLES:
        roles_listbox.insert(tk.END, role)

    def run_process_all_users():
        threading.Thread(target=process_all_users, daemon=True).start()



    APPLICANT_OPTIONS = ["City A", "City B"]
    COUNTY_OPTIONS = ["County X", "County Y", "County Z"]
    ACCESS_LEVELS = ["Primary", "Alternate", "Other", "Authorized Agent"]
    ASSIGNMENT_PRESETS = {
        "Full Access Set": [
            ("City A", "", "Primary"),
            ("", "County Y", "Alternate")
        ],
        "Basic Access Set": [
            ("City B", "", "Other")
        ]
    }


    def open_assignment_editor():
        if selected_index[0] is None:
            messagebox.showerror("Error", "Select a user to edit assignments.")
            return

        def add_assignment():
            app = applicant_cb.get().strip()
            county = county_cb.get().strip()
            level = access_cb.get().strip()
            if (not app and not county) or (app and county):
                messagebox.showerror("Error", "Please specify either Applicant OR County, not both.")
                return
            if not level:
                messagebox.showerror("Error", "Please select Access Level.")
                return

            assignment = (app, county, level)
            if assignment in current_assignments:
                messagebox.showwarning("Duplicate", "This assignment is already added.")
                return

            current_assignments.append(assignment)
            listbox.insert(tk.END, format_assignment(assignment))

        def format_assignment(assignment):
            app, county, level = assignment
            if app:
                return f"Applicant: {app} | Access Level: {level}"
            else:
                return f"County: {county} | Access Level: {level}"

        def apply_preset(preset_name):
            for assignment in ASSIGNMENT_PRESETS[preset_name]:
                if assignment not in current_assignments:
                    current_assignments.append(assignment)
                    listbox.insert(tk.END, format_assignment(assignment))

        def remove_assignment():
            selected = listbox.curselection()
            if not selected:
                return
            idx = selected[0]
            del current_assignments[idx]
            listbox.delete(idx)

        def save_assignments():
            user_key = processing_list.iloc[selected_index[0]]["Email"]
            user_assignments[user_key] = current_assignments.copy()
            win.destroy()

        win = tk.Toplevel()
        win.title("Edit Assignments")
        win.geometry("450x450")
        tk.Label(win, text="Applicant").pack()
        applicant_cb = ttk.Combobox(win, values=APPLICANT_OPTIONS)
        applicant_cb.pack()
        applicant_cb.set("")
        tk.Label(win, text="County").pack()
        county_cb = ttk.Combobox(win, values=COUNTY_OPTIONS)
        county_cb.pack()
        county_cb.set("")


        def filter_applicant(event):
            typed = applicant_cb.get()
            filtered = [x for x in APPLICANT_OPTIONS if typed.lower() in x.lower()]
            applicant_cb['values'] = filtered

        applicant_cb.bind('<KeyRelease>', filter_applicant)
        def filter_county(event):
            typed = county_cb.get()
            filtered = [x for x in COUNTY_OPTIONS if typed.lower() in x.lower()]
            county_cb['values'] = filtered
        county_cb.bind('<KeyRelease>', filter_county)

        user_key = processing_list.iloc[selected_index[0]]["Email"]
        current_assignments = user_assignments.get(user_key, [])[:]




        tk.Label(win, text="Access Level").pack()
        access_cb = ttk.Combobox(win, values=ACCESS_LEVELS)
        access_cb.pack()
        access_cb.set("")

        add_btn = tk.Button(win, text="Add Assignment", command=add_assignment)
        add_btn.pack(pady=5)

        tk.Label(win, text="Presets").pack()
        preset_listbox = tk.Listbox(win, height=5)
        preset_listbox.pack()
        for preset in ASSIGNMENT_PRESETS:
            preset_listbox.insert(tk.END, preset)

        def on_preset_select(event):
            selection = preset_listbox.curselection()
            if not selection:
                return
            preset_name = preset_listbox.get(selection[0])
            apply_preset(preset_name)

        preset_listbox.bind('<<ListboxSelect>>', on_preset_select)

        listbox = tk.Listbox(win, width=60, height=10)
        listbox.pack(pady=5)
        for assignment in current_assignments:
            listbox.insert(tk.END, format_assignment(assignment))

        remove_btn = tk.Button(win, text="Remove Selected Assignment", command=remove_assignment)
        remove_btn.pack(pady=5)

        save_btn = tk.Button(win, text="Save Assignments", command=save_assignments)
        save_btn.pack(pady=10)


    append_btn = tk.Button(root, text="Add to List", command=append_user, bg="blue", fg="white")
    append_btn.grid(row=len(fields)+3, column=0, pady=10)

    process_btn = tk.Button(root, text="Process All", command=run_process_all_users, bg="green", fg="white")
    process_btn.grid(row=len(fields)+3, column=1, pady=10)

    edit_btn = tk.Button(root, text="Edit Selected", command=update_user, bg="orange", fg="black")
    edit_btn.grid(row=len(fields)+4, column=0, pady=5)

    edit_assignments_btn = tk.Button(root, text="Edit Assignments", command=open_assignment_editor, bg="purple", fg="white")
    edit_assignments_btn.grid(row=len(fields)+4, column=1, pady=5)


    def on_closing():
        try:
            driver.quit()
        except Exception:
            pass
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


start_tkinter()