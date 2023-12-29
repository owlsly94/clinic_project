import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import sqlite3

class PatientRecordsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Patient Records")

        # Database connection for user authentication
        self.conn = sqlite3.connect("user_credentials.db")
        self.cursor = self.conn.cursor()
        self.create_user_table()

        # Headline
        self.headline_label = tk.Label(root, text="Patient Records", font=("Helvetica", 16))
        self.headline_label.pack(pady=20)

        # Buttons for Options
        self.add_record_button = tk.Button(root, text="Add Record", command=self.open_add_record_window)
        self.add_record_button.pack(pady=10)

        self.search_records_button = tk.Button(root, text="Search Records", command=self.open_search_records_window)
        self.search_records_button.pack(pady=10)

        self.doctors_button = tk.Button(root, text="Doctors", command=self.authenticate_and_open_doctors)
        self.doctors_button.pack(pady=10)

        self.appointments_button = tk.Button(root, text="Appointments", command=self.open_appointments_window)
        self.appointments_button.pack(pady=10)

        # Center the window
        self.center_window()

    def center_window(self):
        width = 300
        height = 250
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def open_add_record_window(self):
        os.system("python e-med-record.py")

    def open_search_records_window(self):
        os.system("python search-med-records.py")

    def open_appointments_window(self):
        os.system("python appointments.py")

    def create_user_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()

        # Insert default user (admin) if not exists
        self.cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        if not self.cursor.fetchone():
            self.cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin')")
            self.conn.commit()

    def authenticate_and_open_doctors(self):
        username = simpledialog.askstring("Authentication", "Enter Username:")
        password = simpledialog.askstring("Authentication", "Enter Password:", show='*')

        if self.authenticate_user(username, password):
            os.system("python doctors.py")
        else:
            messagebox.showerror("Authentication Failed", "Invalid username or password.")

    def authenticate_user(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        return self.cursor.fetchone() is not None

if __name__ == "__main__":
    root = tk.Tk()
    app = PatientRecordsApp(root)
    root.mainloop()
