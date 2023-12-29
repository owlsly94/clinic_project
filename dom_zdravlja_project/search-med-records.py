import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox

class PatientSearch:
    def __init__(self, root):
        self.root = root
        self.root.title("Patient Search")

        # Database connection
        self.conn = sqlite3.connect("medical_records.db")
        self.cursor = self.conn.cursor()

        # Patient Search Section
        self.patient_search_label = tk.Label(root, text="Patient Search", font=("Helvetica", 16))
        self.patient_search_label.pack(pady=10)

        self.create_search_form()

        # Search Results Section
        self.search_results_label = tk.Label(root, text="Search Results", font=("Helvetica", 16))
        self.search_results_label.pack(pady=10)

        # Create a Treeview widget for displaying search results
        self.tree = ttk.Treeview(root, columns=("Record Number", "Name", "Last Name", "JBMG", "LBO", "Medical Card Number", "Address"), show="headings")
        self.tree.pack()

        # Set column headings
        headings = ["Record Number", "Name", "Last Name", "JBMG", "LBO", "Medical Card Number", "Address"]
        for heading in headings:
            self.tree.heading(heading, text=heading)
            self.tree.column(heading, width=100)  # Adjust width as needed

        # Center the window
        self.center_window()

    def center_window(self):
        width = 800  # Adjust width as needed
        height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_search_form(self):
        self.search_entries = {}
        search_parameters = ["JBMG", "LBO", "Name", "Surname", "Medical Card Number"]

        for parameter in search_parameters:
            tk.Label(self.root, text=parameter).pack()
            entry = tk.Entry(self.root)
            entry.pack()
            self.search_entries[parameter] = entry

        # Search Button
        search_button = tk.Button(self.root, text="Search", command=self.search_patients)
        search_button.pack(pady=10)

    def search_patients(self):
        # Clear previous search results
        self.tree.delete(*self.tree.get_children())

        # Get search parameters
        search_values = [entry.get() for entry in self.search_entries.values()]

        # Build the SQL query
        sql_query = '''
            SELECT record_number, name, last_name, jmbg, lbo, medical_card_number, address
            FROM medical_records
            WHERE jmbg = ? OR lbo = ? OR name = ? OR last_name = ? OR medical_card_number = ?
        '''

        # Execute the query
        self.cursor.execute(sql_query, tuple(search_values))
        results = self.cursor.fetchall()

        if not results:
            messagebox.showinfo("Search Results", "No matching records found.")
            return

        # Display search results in the Treeview widget
        for result in results:
            self.tree.insert("", "end", values=result)

if __name__ == "__main__":
    root = tk.Tk()
    app = PatientSearch(root)
    root.mainloop()
