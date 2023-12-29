import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class EMRSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Electronic Medical Record System")

        # Database connection
        self.conn = sqlite3.connect("medical_records.db")
        self.cursor = self.conn.cursor()

        # Create the medical_records table if it does not exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS medical_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                middle_name TEXT,
                last_name TEXT,
                record_number TEXT,
                jmbg TEXT,
                lbo TEXT,
                medical_card_number TEXT,
                address TEXT,
                phone_number TEXT,
                city TEXT,
                insurance_carriers TEXT,
                insurance_carrier_jmbg TEXT,
                insurance_carrier_lbo TEXT,
                insurance_carrier_name TEXT,
                insurance_carrier_last_name TEXT,
                insurance_type TEXT,
                company_name TEXT,
                company_pib TEXT,
                company_registration_number TEXT,
                sex TEXT,
                marital_status TEXT,
                blood_type TEXT,
                rh_factor TEXT,
                cholesterol INTEGER,
                smoking INTEGER,
                obesity INTEGER,
                hypertension INTEGER,
                diabetes INTEGER,
                alcoholism INTEGER,
                allergy INTEGER,
                general_practice TEXT,
                pediatrician TEXT,
                dentist TEXT,
                gynecologist_urologist TEXT
            )
        ''')

        # Commit the table creation
        self.conn.commit()

        # Create a canvas with a vertical scrollbar
        self.canvas = tk.Canvas(root)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(root, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', self.on_canvas_configure)

        # Create a frame inside the canvas
        self.frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor=tk.NW)

        # Basic Information Section
        self.basic_info_label = tk.Label(self.frame, text="Basic Information", font=("Helvetica", 16))
        self.basic_info_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.create_basic_info_form()

        # Medical Insurance Data Section
        self.medical_insurance_label = tk.Label(self.frame, text="Medical Insurance Data", font=("Helvetica", 16))
        self.medical_insurance_label.grid(row=12, column=0, columnspan=2, pady=10)

        self.create_medical_insurance_form()

        # Employment Data Section
        self.employment_data_label = tk.Label(self.frame, text="Employment Data", font=("Helvetica", 16))
        self.employment_data_label.grid(row=20, column=0, columnspan=2, pady=10)

        self.create_employment_data_form()

        # Personal Information and Medical Info Section
        self.personal_info_label = tk.Label(self.frame, text="Personal Information and Medical Info", font=("Helvetica", 16))
        self.personal_info_label.grid(row=28, column=0, columnspan=2, pady=10)

        self.create_personal_info_form()

        # Risk Factor Section
        self.risk_factor_label = tk.Label(self.frame, text="Risk Factor", font=("Helvetica", 16))
        self.risk_factor_label.grid(row=36, column=0, columnspan=2, pady=10)

        self.create_risk_factor_form()

        # Chosen Doctor Section
        self.chosen_doctor_label = tk.Label(self.frame, text="Chosen Doctor", font=("Helvetica", 16))
        self.chosen_doctor_label.grid(row=44, column=0, columnspan=2, pady=10)

        self.create_chosen_doctor_form()

        # Save Button
        self.save_button = tk.Button(root, text="Save Record", command=self.save_record)
        self.save_button.pack(side=tk.BOTTOM, pady=10)

        # Record Saved Label
        self.record_saved_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.record_saved_label.pack(side=tk.BOTTOM, pady=20)  # 20px gap only below this label

        # Set the frame as the scrollable region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        # Update the scroll region to fit the new size of the canvas
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_basic_info_form(self):
        self.basic_info_labels = ["Name", "Middle Name", "Last Name", "Record Number", "JMBG",
                                  "LBO", "Medical Card Number", "Address", "Phone Number", "City"]

        self.basic_info_entries = {}
        for i, label in enumerate(self.basic_info_labels):
            tk.Label(self.frame, text=label).grid(row=i + 1, column=0)
            self.basic_info_entries[label] = tk.Entry(self.frame)
            self.basic_info_entries[label].grid(row=i + 1, column=1)

    def create_medical_insurance_form(self):
        self.medical_insurance_labels = ["Number of Insurance Carriers", "JMBG of Insurance Carrier",
                                         "LBO of Insurance Carrier", "Name of Insurance Carrier",
                                         "Last Name of Insurance Carrier", "Insurance Type"]

        self.medical_insurance_entries = {}
        for i, label in enumerate(self.medical_insurance_labels):
            tk.Label(self.frame, text=label).grid(row=i + 13, column=0)
            self.medical_insurance_entries[label] = tk.Entry(self.frame)
            self.medical_insurance_entries[label].grid(row=i + 13, column=1)

        # Insurance Type Options
        insurance_type_options = ["State", "Private Domestic", "Private Foreign"]
        self.insurance_type_var = tk.StringVar()
        self.insurance_type_var.set(insurance_type_options[0])
        tk.Label(self.frame, text="Insurance Type").grid(row=19, column=0)
        insurance_type_menu = tk.OptionMenu(self.frame, self.insurance_type_var, *insurance_type_options)
        insurance_type_menu.grid(row=19, column=1)

    def create_employment_data_form(self):
        self.employment_data_labels = ["Company Name", "PIB", "Company Registration Number"]

        self.employment_data_entries = {}
        for i, label in enumerate(self.employment_data_labels):
            tk.Label(self.frame, text=label).grid(row=i + 21, column=0)
            self.employment_data_entries[label] = tk.Entry(self.frame)
            self.employment_data_entries[label].grid(row=i + 21, column=1)

    def create_personal_info_form(self):
        self.personal_info_labels = ["Sex", "Marital Status", "Blood Type", "Rh Factor"]

        self.personal_info_entries = {}
        for i, label in enumerate(self.personal_info_labels):
            tk.Label(self.frame, text=label).grid(row=i + 29, column=0)
            self.personal_info_entries[label] = tk.Entry(self.frame)
            self.personal_info_entries[label].grid(row=i + 29, column=1)

        # Sex Options
        sex_options = ["Male", "Female", "Other"]
        self.sex_var = tk.StringVar()
        self.sex_var.set(sex_options[0])
        tk.Label(self.frame, text="Sex").grid(row=33, column=0)
        sex_menu = tk.OptionMenu(self.frame, self.sex_var, *sex_options)
        sex_menu.grid(row=33, column=1)

        # Blood Type Options
        blood_type_options = ["A", "B", "AB", "O"]
        self.blood_type_var = tk.StringVar()
        self.blood_type_var.set(blood_type_options[0])
        tk.Label(self.frame, text="Blood Type").grid(row=34, column=0)
        blood_type_menu = tk.OptionMenu(self.frame, self.blood_type_var, *blood_type_options)
        blood_type_menu.grid(row=34, column=1)

        # Rh Factor Options
        rh_factor_options = ["Negative", "Positive"]
        self.rh_factor_var = tk.StringVar()
        self.rh_factor_var.set(rh_factor_options[0])
        tk.Label(self.frame, text="Rh Factor").grid(row=35, column=0)
        rh_factor_menu = tk.OptionMenu(self.frame, self.rh_factor_var, *rh_factor_options)
        rh_factor_menu.grid(row=35, column=1)

    def create_risk_factor_form(self):
        self.risk_factor_labels = ["Cholesterol", "Smoking", "Obesity", "Hypertension", "Diabetes", "Alcoholism", "Allergy"]

        self.risk_factor_entries = {}
        for i, label in enumerate(self.risk_factor_labels):
            tk.Label(self.frame, text=label).grid(row=i + 37, column=0)
            self.risk_factor_entries[label] = tk.IntVar()
            tk.Checkbutton(self.frame, variable=self.risk_factor_entries[label]).grid(row=i + 37, column=1)

    def create_chosen_doctor_form(self):
        self.chosen_doctor_labels = ["General Practice", "Pediatrician", "Dentist", "Gynecologist/Urologist"]

        self.chosen_doctor_entries = {}
        for i, label in enumerate(self.chosen_doctor_labels):
            tk.Label(self.frame, text=label).grid(row=i + 45, column=0)
            self.chosen_doctor_entries[label] = tk.Entry(self.frame)
            self.chosen_doctor_entries[label].grid(row=i + 45, column=1)

    def save_record(self):
        # Get data from entries
        basic_info_data = [self.basic_info_entries[label].get() for label in self.basic_info_labels]
        medical_insurance_data = [self.medical_insurance_entries[label].get() for label in self.medical_insurance_labels]
        medical_insurance_data.append(self.insurance_type_var.get())
        employment_data = [self.employment_data_entries[label].get() for label in self.employment_data_labels]
        personal_info_data = [self.sex_var.get(), self.personal_info_entries["Marital Status"].get(),
                              self.blood_type_var.get(), self.rh_factor_var.get()]
        risk_factor_data = [self.risk_factor_entries[label].get() for label in self.risk_factor_labels]
        chosen_doctor_data = [self.chosen_doctor_entries[label].get() for label in self.chosen_doctor_labels]

        # Insert data into the database
        # Remove one placeholder for "Insurance Type"
        
        self.cursor.execute('''
            INSERT INTO medical_records (
                name, middle_name, last_name, record_number, jmbg, lbo, medical_card_number, address, phone_number, city,
                insurance_carriers, insurance_carrier_jmbg, insurance_carrier_lbo, insurance_carrier_name,
                insurance_carrier_last_name, insurance_type, company_name, company_pib, company_registration_number,
                sex, marital_status, blood_type, rh_factor, cholesterol, smoking, obesity, hypertension, diabetes,
                alcoholism, allergy, general_practice, pediatrician, dentist, gynecologist_urologist
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', tuple(basic_info_data + medical_insurance_data + employment_data + personal_info_data +
                    risk_factor_data + chosen_doctor_data[:-1]))  # Exclude the last element (Insurance Type)


        # Commit changes to the database
        self.conn.commit()

        # Clear all entries
        for entry in self.basic_info_entries.values():
            entry.delete(0, tk.END)

        for entry in self.medical_insurance_entries.values():
            entry.delete(0, tk.END)

        for entry in self.employment_data_entries.values():
            entry.delete(0, tk.END)

        for entry in self.personal_info_entries.values():
            entry.delete(0, tk.END)

        for entry in self.chosen_doctor_entries.values():
            entry.delete(0, tk.END)

        for entry in self.risk_factor_entries.values():
            entry.set(0)

        # Update the record saved label
        self.record_saved_label.config(text="Record saved successfully!")

        # Display a success message (for demo purposes)
        messagebox.showinfo("Success", "Record saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = EMRSystem(root)
    root.mainloop()
