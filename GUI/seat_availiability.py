import tkinter as tk
from tkinter import messagebox
import sqlite3
import os


def run():
    root = tk.Tk()
    app = SeatAvailabilityApp(root)
    root.mainloop()


class SeatAvailabilityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Seat Availability")
        self.root.geometry("700x420")

        # Connect to project database file
        script_dir = os.path.dirname(__file__)
        db_path = os.path.abspath(os.path.join(script_dir, '..', 'airport.db'))
        if not os.path.exists(db_path):
            messagebox.showerror("DB Error", f"Database not found: {db_path}")
            self.root.destroy()
            return
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        self.create_widgets()

    def setup_database(self):
        # minimal LEG_INSTANCE and SEAT tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS LEG_INSTANCE (
                Flight_no TEXT,
                Date TEXT,
                Leg_no INTEGER,
                Airplane_id INTEGER,
                Available_seats INTEGER
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS SEAT (
                Seat_no TEXT,
                Flight_no TEXT,
                Date TEXT,
                Leg_no INTEGER,
                Customer_name TEXT,
                Phone TEXT
            )
        ''')

        sample_instances = [
            ('AA3478','2026-05-01',1,1,180),
            ('AA3478','2026-05-01',2,1,180),
            ('UA202','2026-05-02',1,2,120),
        ]

        sample_seats = [
            ('12A','AA3478','2026-05-01',1,'John Doe','1234567890'),
            ('12B','AA3478','2026-05-01',1,'Jane Roe','0987654321'),
        ]

        for row in sample_instances:
            try:
                self.cursor.execute('INSERT INTO LEG_INSTANCE VALUES (?, ?, ?, ?, ?)', row)
            except sqlite3.IntegrityError:
                pass
        for row in sample_seats:
            try:
                self.cursor.execute('INSERT INTO SEAT VALUES (?, ?, ?, ?, ?, ?)', row)
            except sqlite3.IntegrityError:
                pass
        self.conn.commit()

    def create_widgets(self):
        header_frame = tk.Frame(self.root, bg='#f0f0f0', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        def go_back():
            self.root.destroy()
            try:
                import Main_Menu as mm
            except Exception as e:
                messagebox.showerror("Error", f"Could not open main menu: {e}")
                return
            if hasattr(mm, 'run'):
                try:
                    mm.run()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to open main menu: {e}")

        back_btn = tk.Button(header_frame, text="← Back", command=go_back, font=('Arial', 10), bg='white', relief=tk.RAISED, width=10)
        back_btn.pack(side=tk.LEFT, padx=10, pady=10)

        title_label = tk.Label(header_frame, text="Seat Availability", font=('Arial', 16, 'bold'), bg='#f0f0f0')
        title_label.pack(side=tk.LEFT, padx=20)

        content = tk.Frame(self.root)
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=12)

        # Input fields
        form = tk.Frame(content)
        form.pack(fill=tk.X)

        flight_label = tk.Label(form, text="Flight number:", font=('Arial', 11))
        flight_label.grid(row=0, column=0, sticky='w')
        self.flight_entry = tk.Entry(form, font=('Arial', 12), width=30)
        self.flight_entry.grid(row=0, column=1, padx=8, pady=4)

        date_label = tk.Label(form, text="Date (YYYY-MM-DD):", font=('Arial', 11))
        date_label.grid(row=1, column=0, sticky='w')
        self.date_entry = tk.Entry(form, font=('Arial', 12), width=30)
        self.date_entry.grid(row=1, column=1, padx=8, pady=4)

        search_btn = tk.Button(form, text="Check", command=self.check_availability, font=('Arial', 11), bg='#4CAF50', fg='white')
        search_btn.grid(row=0, column=2, rowspan=2, padx=8)

        # Results frames
        results_outer = tk.Frame(content)
        results_outer.pack(fill=tk.BOTH, expand=True, pady=(12,0))

        left = tk.Frame(results_outer, relief=tk.SUNKEN, borderwidth=1)
        left.pack(fill=tk.BOTH, expand=True)
        left_title = tk.Label(left, text="Available Seats", font=('Arial', 12, 'bold'))
        left_title.pack(anchor='nw', padx=8, pady=8)
        self.left_text = tk.Text(left, font=('Courier', 10), state=tk.DISABLED)
        self.left_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0,8))
        # tag for error messages (red)
        self.left_text.tag_configure('error', foreground='red')

    def check_availability(self):
        flight = self.flight_entry.get().strip()
        date = self.date_entry.get().strip()

        if not flight or not date:
            messagebox.showwarning("Input Error", "Please enter flight number and date")
            return

        # Query LEG_INSTANCE for available seats per leg
        self.cursor.execute('''
            SELECT Leg_no, Available_seats FROM LEG_INSTANCE
            WHERE Flight_no=? AND Date=?
            ORDER BY Leg_no
        ''', (flight, date))
        rows = self.cursor.fetchall()

        self.left_text.config(state=tk.NORMAL)
        self.left_text.delete(1.0, tk.END)

        if rows:
            total = 0
            self.left_text.insert(tk.END, "Leg_no | Available_seats\n")
            self.left_text.insert(tk.END, "-------------------------\n")
            for leg_no, avail in rows:
                self.left_text.insert(tk.END, f"{leg_no:6} | {avail:15}\n")
                try:
                    total += int(avail)
                except Exception:
                    pass
            self.left_text.insert(tk.END, f"\nTotal available seats (sum across legs): {total}\n")
        else:
            self.left_text.insert(tk.END, "Data not found. Try again.", 'error')

        self.left_text.config(state=tk.DISABLED)

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()


if __name__ == '__main__':
    run()
