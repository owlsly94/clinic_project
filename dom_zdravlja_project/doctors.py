import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox

class DoctorRecords:
    def __init__(self, root):
        self.root = root
        self.root.title("Doctor Records")

        # Database connection
        self.conn = sqlite3.connect("doctor_records.db")
        self.cursor = self.conn.cursor()

        # Create the doctors table if it doesn't exist
        self.create_doctors_table()

        # Doctor Records Section
        self.doctor_records_label = tk.Label(root, text="Doctor Records", font=("Helvetica", 16))
        self.doctor_records_label.pack(pady=10)

        # Add Doctor Form
        self.create_add_doctor_form()

        # Remove Doctor Form
        self.create_remove_doctor_form()

        # Search Doctor Form
        self.create_search_doctor_form()

        # Display Doctor Records
        self.create_doctor_records_display()

        # Center the window
        self.center_window()

    def create_doctors_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctors (
                doctor_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                specialty TEXT,
                office_number TEXT,
                phone_number TEXT,
                address TEXT
            )
        ''')
        self.conn.commit()

    def center_window(self):
        width = 800
        height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_add_doctor_form(self):
        tk.Label(self.root, text="Add Doctor", font=("Helvetica", 14)).pack()

        self.add_doctor_entries = {}
        add_doctor_labels = ["Name", "Last Name", "Specialty", "Office Number", "Phone Number", "Address"]

        for label in add_doctor_labels:
            tk.Label(self.root, text=label).pack()
            entry = tk.Entry(self.root)
            entry.pack()
            self.add_doctor_entries[label] = entry

        # Add Doctor Button
        add_doctor_button = tk.Button(self.root, text="Add Doctor", command=self.add_doctor)
        add_doctor_button.pack(pady=10)

    def create_remove_doctor_form(self):
        tk.Label(self.root, text="Remove Doctor", font=("Helvetica", 14)).pack()

        # Remove Doctor ID Entry
        tk.Label(self.root, text="Doctor ID to Remove").pack()
        self.remove_doctor_id_entry = tk.Entry(self.root)
        self.remove_doctor_id_entry.pack()

        # Remove Doctor Button
        remove_doctor_button = tk.Button(self.root, text="Remove Doctor", command=self.remove_doctor)
        remove_doctor_button.pack(pady=10)

    def create_search_doctor_form(self):
        tk.Label(self.root, text="Search Doctor", font=("Helvetica", 14)).pack()

        # Search Doctor Name Entry
        tk.Label(self.root, text="Doctor Name to Search").pack()
        self.search_doctor_name_entry = tk.Entry(self.root)
        self.search_doctor_name_entry.pack()

        # Search Doctor Button
        search_doctor_button = tk.Button(self.root, text="Search Doctor", command=self.search_doctor)
        search_doctor_button.pack(pady=10)

    def create_doctor_records_display(self):
        tk.Label(self.root, text="Doctor Records", font=("Helvetica", 14)).pack()

        # Display Doctor Records in a Treeview
        columns = ["Doctor ID", "Name", "Last Name", "Specialty", "Office Number", "Phone Number", "Address"]
        self.doctor_treeview = ttk.Treeview(self.root, columns=columns, show="headings")

        for col in columns:
            self.doctor_treeview.heading(col, text=col)
            self.doctor_treeview.column(col, width=100)

        self.doctor_treeview.pack()

    def add_doctor(self):
        # Get data from entries
        doctor_data = [entry.get() for entry in self.add_doctor_entries.values()]

        # Insert data into the doctors table
        self.cursor.execute('''
            INSERT INTO doctors (name, last_name, specialty, office_number, phone_number, address)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', tuple(doctor_data))

        # Commit changes to the database
        self.conn.commit()

        # Clear entry fields
        for entry in self.add_doctor_entries.values():
            entry.delete(0, tk.END)

        # Refresh the doctor records display
        self.display_doctor_records()

        # Display a success message (for demo purposes)
        messagebox.showinfo("Success", "Doctor record added successfully!")

    def remove_doctor(self):
        # Get doctor ID to remove
        doctor_id_to_remove = self.remove_doctor_id_entry.get()

        # Remove the doctor record from the database
        self.cursor.execute('DELETE FROM doctors WHERE doctor_id = ?', (doctor_id_to_remove,))

        # Commit changes to the database
        self.conn.commit()

        # Clear entry field
        self.remove_doctor_id_entry.delete(0, tk.END)

        # Refresh the doctor records display
        self.display_doctor_records()

        # Display a success message (for demo purposes)
        messagebox.showinfo("Success", "Doctor record removed successfully!")

    def search_doctor(self):
        # Get doctor name to search
        doctor_name_to_search = self.search_doctor_name_entry.get()

        # Build the SQL query
        sql_query = '''
            SELECT * FROM doctors WHERE name LIKE ?
        '''

        # Execute the query
        self.cursor.execute(sql_query, (f"%{doctor_name_to_search}%",))
        results = self.cursor.fetchall()

        # Display search results in the Treeview
        self.display_search_results(results)

    def display_doctor_records(self):
        # Clear previous records in the Treeview
        for item in self.doctor_treeview.get_children():
            self.doctor_treeview.delete(item)

        # Query all records from the doctors table
        self.cursor.execute('SELECT * FROM doctors')
        records = self.cursor.fetchall()

        # Insert records into the Treeview
        for record in records:
            self.doctor_treeview.insert("", tk.END, values=record)

    def display_search_results(self, results):
        # Clear previous search results in the Treeview
        for item in self.doctor_treeview.get_children():
            self.doctor_treeview.delete(item)

        # Insert search results into the Treeview
        for result in results:
            self.doctor_treeview.insert("", tk.END, values=result)

if __name__ == "__main__":
    root = tk.Tk()
    app = DoctorRecords(root)
    root.mainloop()
