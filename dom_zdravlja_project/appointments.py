import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from tkcalendar import Calendar

class AppointmentsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Appointments")

        # Database connection for appointments
        self.conn_appointments = sqlite3.connect("appointments.db")
        self.cursor_appointments = self.conn_appointments.cursor()
        self.create_appointments_table()

        # Calendar Section
        self.calendar_frame = ttk.Frame(root)
        self.calendar_frame.pack(pady=20)

        tk.Label(self.calendar_frame, text="Select Date:").grid(row=0, column=0, padx=5)
        self.date_var = tk.StringVar()
        self.date_entry = tk.Entry(self.calendar_frame, textvariable=self.date_var)
        self.date_entry.grid(row=0, column=1, padx=5)

        date_button = tk.Button(self.calendar_frame, text="Select Date", command=self.select_date)
        date_button.grid(row=0, column=2, padx=5)

        # Patient Information Section
        self.patient_frame = ttk.Frame(root)
        self.patient_frame.pack(pady=20)

        tk.Label(self.patient_frame, text="Patient Name:").grid(row=0, column=0, padx=5)
        self.patient_name_entry = tk.Entry(self.patient_frame)
        self.patient_name_entry.grid(row=0, column=1, padx=5)

        tk.Label(self.patient_frame, text="Patient Last Name:").grid(row=0, column=2, padx=5)
        self.patient_last_name_entry = tk.Entry(self.patient_frame)
        self.patient_last_name_entry.grid(row=0, column=3, padx=5)

        tk.Label(self.patient_frame, text="Patient JMBG:").grid(row=0, column=4, padx=5)
        self.patient_jmbg_entry = tk.Entry(self.patient_frame)
        self.patient_jmbg_entry.grid(row=0, column=5, padx=5)

        tk.Label(self.patient_frame, text="Patient Phone Number:").grid(row=0, column=6, padx=5)
        self.patient_phone_entry = tk.Entry(self.patient_frame)
        self.patient_phone_entry.grid(row=0, column=7, padx=5)

        # Doctor Information Section
        self.doctor_frame = ttk.Frame(root)
        self.doctor_frame.pack(pady=20)

        tk.Label(self.doctor_frame, text="Doctor Name:").grid(row=0, column=0, padx=5)
        self.doctor_name_entry = tk.Entry(self.doctor_frame)
        self.doctor_name_entry.grid(row=0, column=1, padx=5)

        tk.Label(self.doctor_frame, text="Doctor Last Name:").grid(row=0, column=2, padx=5)
        self.doctor_last_name_entry = tk.Entry(self.doctor_frame)
        self.doctor_last_name_entry.grid(row=0, column=3, padx=5)

        tk.Label(self.doctor_frame, text="Doctor Office Number:").grid(row=0, column=4, padx=5)
        self.doctor_office_entry = tk.Entry(self.doctor_frame)
        self.doctor_office_entry.grid(row=0, column=5, padx=5)

        # Make Appointment Button
        make_appointment_button = tk.Button(root, text="Make Appointment", command=self.make_appointment)
        make_appointment_button.pack(pady=10)

        # Appointments Display
        self.appointments_frame = ttk.Frame(root, borderwidth=2, relief="solid")
        self.appointments_frame.pack(pady=20)

        # Display Appointments
        self.display_appointments()

        # Cancel Appointment Button
        cancel_appointment_button = tk.Button(root, text="Cancel Appointment", command=self.cancel_appointment)
        cancel_appointment_button.pack(pady=10)

    def select_date(self):
        cal = Calendar(self.root, selectmode="day", date_pattern="yyyy-mm-dd")
        selected_date = cal.selection_get()
        self.date_var.set(selected_date)

    def make_appointment(self):
        # Get the values entered by the user
        date = self.date_var.get()
        patient_name = self.patient_name_entry.get()
        patient_last_name = self.patient_last_name_entry.get()
        patient_jmbg = self.patient_jmbg_entry.get()
        patient_phone = self.patient_phone_entry.get()
        doctor_name = self.doctor_name_entry.get()
        doctor_last_name = self.doctor_last_name_entry.get()
        doctor_office = self.doctor_office_entry.get()

        # Validate that all fields are filled
        if not all([date, patient_name, patient_last_name, patient_jmbg, patient_phone, doctor_name, doctor_last_name, doctor_office]):
            messagebox.showinfo("Make Appointment", "Please fill in all fields.")
            return

        # Insert the appointment into the database
        self.cursor_appointments.execute('''
            INSERT INTO appointments (date, patient_name, patient_last_name, patient_jmbg, patient_phone, doctor_name, doctor_last_name, doctor_office)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (date, patient_name, patient_last_name, patient_jmbg, patient_phone, doctor_name, doctor_last_name, doctor_office))

        # Commit changes to the database
        self.conn_appointments.commit()

        # Display success message
        messagebox.showinfo("Make Appointment", "Appointment made successfully.")

        # Update the appointments display
        self.display_appointments()

    def display_appointments(self):
        # Clear previous appointments
        for widget in self.appointments_frame.winfo_children():
            widget.destroy()

        # Build the SQL query
        sql_query = '''
            SELECT date, patient_name, patient_last_name, doctor_name, doctor_last_name, doctor_office
            FROM appointments
            ORDER BY date
        '''

        # Execute the query
        self.cursor_appointments.execute(sql_query)
        appointments = self.cursor_appointments.fetchall()

        if not appointments:
            ttk.Label(self.appointments_frame, text="No Appointments", font=("Helvetica", 12)).pack(pady=10)
            return

        # Display appointments horizontally
        labels = ["Date", "Patient Name", "Last Name", "Doctor Name", "Doctor Last Name", "Office Number"]
        for i, label in enumerate(labels):
            ttk.Label(self.appointments_frame, text=label, font=("Helvetica", 12)).grid(row=0, column=i, padx=5, pady=2)

        for i, appointment in enumerate(appointments, start=1):
            for j, value in enumerate(appointment):
                ttk.Label(self.appointments_frame, text=value, font=("Helvetica", 12)).grid(row=i, column=j, padx=5, pady=2)

    def cancel_appointment(self):
        selected_appointment = simpledialog.askstring("Cancel Appointment", "Enter the date of the appointment to cancel:")

        if not selected_appointment:
            return

        # Remove the appointment from the database
        self.cursor_appointments.execute('''
            DELETE FROM appointments
            WHERE date = ?
        ''', (selected_appointment,))

        # Commit changes to the database
        self.conn_appointments.commit()

        # Display success message
        messagebox.showinfo("Cancel Appointment", "Appointment canceled successfully.")

        # Update the appointments display
        self.display_appointments()

    def create_appointments_table(self):
        self.cursor_appointments.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE,
                patient_name TEXT,
                patient_last_name TEXT,
                patient_jmbg TEXT,
                patient_phone TEXT,
                doctor_name TEXT,
                doctor_last_name TEXT,
                doctor_office TEXT
            )
        ''')
        self.conn_appointments.commit()

if __name__ == "__main__":
    root = tk.Tk()
    app = AppointmentsApp(root)
    root.mainloop()
