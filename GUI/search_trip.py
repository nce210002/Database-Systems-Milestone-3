import tkinter as tk
from tkinter import messagebox
import sqlite3
import os


def run():
    root = tk.Tk()
    app = TripSearchApp(root)
    root.mainloop()


class TripSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Search Trip")
        self.root.geometry("700x520")

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
        # FLIGHT_LEG table matches the CLI example
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS FLIGHT_LEG (
                Flight_no TEXT PRIMARY KEY,
                Departure_airport TEXT,
                Arrival_airport TEXT,
                Departure_time TEXT,
                Arrival_time TEXT,
                Status TEXT
            )
        ''')

        sample_legs = [
            ('AA101', 'New York', 'Los Angeles', '08:00', '11:30', 'On Time'),
            ('AA505', 'New York', 'Chicago', '09:00', '10:45', 'On Time'),
            ('UA606', 'Chicago', 'Los Angeles', '12:00', '14:30', 'On Time'),
            ('UA202', 'Chicago', 'Denver', '10:15', '11:45', 'Boarding'),
            ('DL707', 'Atlanta', 'Dallas', '13:15', '15:00', 'On Time'),
            ('SW808', 'Dallas', 'Los Angeles', '18:00', '20:30', 'On Time'),
            ('DL303', 'Atlanta', 'Miami', '14:00', '15:30', 'Delayed'),
            ('SW404', 'Dallas', 'Houston', '16:30', '17:45', 'On Time'),
        ]

        # Insert sample legs (ignore errors if rerun)
        for leg in sample_legs:
            try:
                self.cursor.execute('INSERT INTO FLIGHT_LEG VALUES (?, ?, ?, ?, ?, ?)', leg)
            except sqlite3.IntegrityError:
                pass
        self.conn.commit()

    def create_widgets(self):
        header_frame = tk.Frame(self.root, bg='#f0f0f0', height=60)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
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

        title_label = tk.Label(header_frame, text="Search Trip", font=('Arial', 16, 'bold'), bg='#f0f0f0')
        title_label.pack(side=tk.LEFT, padx=20, pady=10)

        content_frame = tk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=16)

        # Input area
        input_frame = tk.Frame(content_frame)
        input_frame.pack(fill=tk.X, pady=(0, 12))

        # From
        from_label = tk.Label(input_frame, text="From airport:", font=('Arial', 11), anchor='w')
        from_label.grid(row=0, column=0, sticky='w')
        self.from_entry = tk.Entry(input_frame, font=('Arial', 12), width=30)
        self.from_entry.grid(row=0, column=1, padx=10, pady=4)

        # To
        to_label = tk.Label(input_frame, text="To airport:", font=('Arial', 11), anchor='w')
        to_label.grid(row=1, column=0, sticky='w')
        self.to_entry = tk.Entry(input_frame, font=('Arial', 12), width=30)
        self.to_entry.grid(row=1, column=1, padx=10, pady=4)

        # Search button
        search_btn = tk.Button(input_frame, text="Search Trip", command=self.search_trip, font=('Arial', 11), bg='#4CAF50', fg='white', padx=14, pady=6)
        search_btn.grid(row=0, column=2, rowspan=2, padx=8)

        # Results area split into two columns
        results_outer = tk.Frame(content_frame)
        results_outer.pack(fill=tk.BOTH, expand=True)

        left_frame = tk.Frame(results_outer, relief=tk.SUNKEN, borderwidth=1)
        left_frame.pack(fill=tk.BOTH, expand=True)

        # Results area (single pane for both data and messages)
        left_title = tk.Label(left_frame, text="Flight Info", font=('Arial', 12, 'bold'))
        left_title.pack(anchor='nw', padx=8, pady=8)

        self.left_text = tk.Text(left_frame, font=('Courier', 10), state=tk.DISABLED)
        self.left_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0,8))
        # tag for error messages (red)
        self.left_text.tag_configure('error', foreground='red')

        # Helpful note at bottom
        note = tk.Label(content_frame, text="Direct Flights and Connecting Flights (if any).", font=('Arial', 10))
        note.pack(anchor='w', pady=(6,0))

        # bind Enter to search
        self.from_entry.bind('<Return>', lambda e: self.search_trip())
        self.to_entry.bind('<Return>', lambda e: self.search_trip())

    def search_trip(self):
        src = self.from_entry.get().strip()
        dst = self.to_entry.get().strip()

        if not src or not dst:
            messagebox.showwarning("Input Error", "Please enter both origin and destination airports")
            return

        # Direct flights query using FLIGHT_LEG (use schema column names)
        self.cursor.execute(
            """
            SELECT Flight_no, Leg_no, Departure_airport, Arrival_airport, Dep_time, Arr_time
            FROM FLIGHT_LEG
            WHERE Departure_airport=? AND Arrival_airport=?
            """,
            (src, dst)
        )
        direct = self.cursor.fetchall()

        # Connecting flights: two legs where f1.Arrival_airport = f2.Departure_airport
        # Select leg numbers and dep/arr times using schema column names
        self.cursor.execute(
                        """
                        SELECT f1.Flight_no, f1.Leg_no, f1.Departure_airport, f1.Arrival_airport, f1.Dep_time, f1.Arr_time,
                                     f2.Flight_no, f2.Leg_no, f2.Departure_airport, f2.Arrival_airport, f2.Dep_time, f2.Arr_time
                        FROM FLIGHT_LEG f1 JOIN FLIGHT_LEG f2
                            ON f1.Arrival_airport = f2.Departure_airport
                        WHERE f1.Departure_airport=? AND f2.Arrival_airport=?
                        """,
                        (src, dst)
                )
        connecting = self.cursor.fetchall()

        # display
        self.left_text.config(state=tk.NORMAL)
        self.left_text.delete(1.0, tk.END)

        if direct:
            self.left_text.insert(tk.END, "Direct Flights:\n\n")
            headers = ['Flight_no', 'Leg', 'Departure', 'Arrival', 'Dep_time', 'Arr_time']
            header_line = " | ".join(f"{h:12}" for h in headers)
            self.left_text.insert(tk.END, header_line + "\n")
            self.left_text.insert(tk.END, "-" * len(header_line) + "\n")
            for r in direct:
                line = " | ".join(f"{str(v):12}" for v in r)
                self.left_text.insert(tk.END, line + "\n")
            self.left_text.insert(tk.END, "\n")

        if connecting:
            self.left_text.insert(tk.END, "Connecting Flights (2-leg):\n\n")
            # include leg numbers and use explicit column widths for alignment
            headers = ['f1_no','f1_leg','f1_dep','f1_arr','f1_dep_time','f1_arr_time', 'f2_no','f2_leg','f2_dep','f2_arr','f2_dep_time','f2_arr_time']
            widths = [10,4,6,6,11,11,10,4,6,6,11,11]
            header_line = " | ".join(f"{h:{w}}" for h,w in zip(headers,widths))
            self.left_text.insert(tk.END, header_line + "\n")
            self.left_text.insert(tk.END, "-" * len(header_line) + "\n")
            for row in connecting:
                # row: (f1_no, f1_leg, f1_dep, f1_arr, f1_dep_time, f1_arr_time, f2_no, f2_leg, f2_dep, f2_arr, f2_dep_time, f2_arr_time)
                line = " | ".join(f"{str(v):{w}}" for v,w in zip(row,widths))
                self.left_text.insert(tk.END, line + "\n")

        if not direct and not connecting:
            self.left_text.insert(tk.END, "Unfortunately, the trip is not available. Try a different one.", 'error')

        self.left_text.config(state=tk.DISABLED)

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()


if __name__ == '__main__':
    run()
