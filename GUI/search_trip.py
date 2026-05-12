import tkinter as tk
from tkinter import messagebox
import sqlite3


def run():
    root = tk.Tk()
    app = TripSearchApp(root)
    root.mainloop()


class TripSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Search Trip")
        self.root.geometry("700x520")

        # In-memory database for UI demo
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.setup_database()

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
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,8))

        right_frame = tk.Frame(results_outer, relief=tk.SUNKEN, borderwidth=1, width=220)
        right_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Left: Available results
        left_title = tk.Label(left_frame, text="If available", font=('Arial', 12, 'bold'))
        left_title.pack(anchor='nw', padx=8, pady=8)

        self.left_text = tk.Text(left_frame, font=('Courier', 10), state=tk.DISABLED)
        self.left_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0,8))

        # Right: Unavailable / messages
        right_title = tk.Label(right_frame, text="If not", font=('Arial', 12, 'bold'))
        right_title.pack(anchor='nw', padx=8, pady=8)

        self.right_text = tk.Text(right_frame, font=('Arial', 10), height=10, state=tk.DISABLED, wrap=tk.WORD)
        self.right_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0,8))

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

        # Direct flights query using FLIGHT_LEG
        self.cursor.execute(
            """
            SELECT * FROM FLIGHT_LEG
            WHERE Departure_airport=? AND Arrival_airport=?
            """,
            (src, dst)
        )
        direct = self.cursor.fetchall()

        # Connecting flights: two legs where f1.Arrival_airport = f2.Departure_airport
        self.cursor.execute(
            """
            SELECT f1.Flight_no, f1.Departure_airport, f1.Arrival_airport, f2.Flight_no, f2.Arrival_airport
            FROM FLIGHT_LEG f1, FLIGHT_LEG f2
            WHERE f1.Arrival_airport = f2.Departure_airport
              AND f1.Departure_airport=? AND f2.Arrival_airport=?
            """,
            (src, dst)
        )
        connecting = self.cursor.fetchall()

        # display
        self.left_text.config(state=tk.NORMAL)
        self.left_text.delete(1.0, tk.END)

        self.right_text.config(state=tk.NORMAL)
        self.right_text.delete(1.0, tk.END)

        if direct:
            self.left_text.insert(tk.END, "Direct Flights:\n\n")
            headers = ['Flight_no', 'Departure', 'Arrival', 'Dep_time', 'Arr_time', 'Status']
            header_line = " | ".join(f"{h:12}" for h in headers)
            self.left_text.insert(tk.END, header_line + "\n")
            self.left_text.insert(tk.END, "-" * len(header_line) + "\n")
            for r in direct:
                line = " | ".join(f"{str(v):12}" for v in r)
                self.left_text.insert(tk.END, line + "\n")
            self.left_text.insert(tk.END, "\n")

        if connecting:
            self.left_text.insert(tk.END, "Connecting Flights (2-leg):\n\n")
            self.left_text.insert(tk.END, "f1_Flight_no | f1_Dep | f1_Arr | f2_Flight_no | f2_Arr\n")
            self.left_text.insert(tk.END, "-" * 60 + "\n")
            for row in connecting:
                # row: (f1_no, f1_dep, f1_arr, f2_no, f2_arr)
                self.left_text.insert(tk.END, " | ".join(f"{str(v):12}" for v in row) + "\n")

        if not direct and not connecting:
            self.right_text.insert(tk.END, "Unfortunately, the trip is not available. Try a different one.")

        self.left_text.config(state=tk.DISABLED)
        self.right_text.config(state=tk.DISABLED)

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()


if __name__ == '__main__':
    run()
