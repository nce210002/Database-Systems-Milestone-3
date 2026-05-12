import tkinter as tk
from tkinter import messagebox
import sqlite3
import os


def run():
    root = tk.Tk()
    app = PassengerItineraryApp(root)
    root.mainloop()


class PassengerItineraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Passenger Itinerary")
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
        # Minimal FLIGHT_LEG and SEAT tables to demo passenger itinerary
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS FLIGHT_LEG (
                Flight_no TEXT,
                Leg_no INTEGER,
                Departure_airport TEXT,
                Arrival_airport TEXT,
                Dep_time TEXT,
                Arr_time TEXT,
                PRIMARY KEY (Flight_no, Leg_no)
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

        sample_legs = [
            ('AA3478', 1, 'DFW', 'SFO', '08:00', '10:30'),
            ('AA3478', 2, 'SFO', 'LAX', '12:00', '13:30'),
            ('UA202', 1, 'ORD', 'DEN', '10:15', '11:45'),
        ]

        sample_seats = [
            ('12A', 'AA3478', '2026-05-01', 1, 'John Doe', '1234567890'),
            ('14C', 'AA3478', '2026-05-01', 2, 'John Doe', '1234567890'),
            ('3B', 'UA202', '2026-05-02', 1, 'Jane Roe', '5555555555'),
        ]

        for leg in sample_legs:
            try:
                self.cursor.execute('INSERT INTO FLIGHT_LEG VALUES (?, ?, ?, ?, ?, ?)', leg)
            except sqlite3.IntegrityError:
                pass

        for seat in sample_seats:
            try:
                self.cursor.execute('INSERT INTO SEAT VALUES (?, ?, ?, ?, ?, ?)', seat)
            except sqlite3.IntegrityError:
                pass

        self.conn.commit()

    def create_widgets(self):
        header = tk.Frame(self.root, bg='#f0f0f0', height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

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

        back_btn = tk.Button(header, text="← Back", command=go_back, font=('Arial', 10), bg='white', relief=tk.RAISED, width=10)
        back_btn.pack(side=tk.LEFT, padx=10, pady=10)

        title = tk.Label(header, text="Passenger Itinerary", font=('Arial', 16, 'bold'), bg='#f0f0f0')
        title.pack(side=tk.LEFT, padx=20)

        body = tk.Frame(self.root)
        body.pack(fill=tk.BOTH, expand=True, padx=20, pady=12)

        # search input
        form = tk.Frame(body)
        form.pack(fill=tk.X)

        name_label = tk.Label(form, text="Search passenger's name:", font=('Arial', 11))
        name_label.grid(row=0, column=0, sticky='w')
        self.name_entry = tk.Entry(form, font=('Arial', 12), width=40)
        self.name_entry.grid(row=0, column=1, padx=8)

        search_btn = tk.Button(form, text="Search", command=self.search_passenger, font=('Arial', 11), bg='#4CAF50', fg='white')
        search_btn.grid(row=0, column=2, padx=8)

        # results split
        results = tk.Frame(body)
        results.pack(fill=tk.BOTH, expand=True, pady=(12,0))

        left = tk.Frame(results, relief=tk.SUNKEN, borderwidth=1)
        left.pack(fill=tk.BOTH, expand=True)
        left_title = tk.Label(left, text="Passenger Flights: ", font=('Arial', 12, 'bold'))
        left_title.pack(anchor='nw', padx=8, pady=8)
        self.left_text = tk.Text(left, font=('Courier', 10), state=tk.DISABLED)
        self.left_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0,8))
        # tag for error messages (red)
        self.left_text.tag_configure('error', foreground='red')

        self.name_entry.bind('<Return>', lambda e: self.search_passenger())

    def search_passenger(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter a passenger name")
            return

        # Query SEAT joined with FLIGHT_LEG to list flights for the passenger
        self.cursor.execute('''
            SELECT s.Flight_no, s.Date, s.Leg_no, f.Departure_airport, f.Arrival_airport, f.Dep_time, f.Arr_time
            FROM SEAT s LEFT JOIN FLIGHT_LEG f
              ON s.Flight_no = f.Flight_no AND s.Leg_no = f.Leg_no
            WHERE s.Customer_name = ?
            ORDER BY s.Date, s.Flight_no, s.Leg_no
        ''', (name,))

        rows = self.cursor.fetchall()

        self.left_text.config(state=tk.NORMAL)
        self.left_text.delete(1.0, tk.END)

        if rows:
            self.left_text.insert(tk.END, "Flight_no | Date       | Leg | From -> To | Dep - Arr\n")
            self.left_text.insert(tk.END, "-" * 80 + "\n")
            for r in rows:
                flight_no, date, leg_no, dep, arr, dep_t, arr_t = r
                dep = dep or 'N/A'
                arr = arr or 'N/A'
                dep_t = dep_t or ''
                arr_t = arr_t or ''
                line = f"{flight_no:9} | {date:10} | {leg_no:3} | {dep} -> {arr} | {dep_t}-{arr_t}\n"
                self.left_text.insert(tk.END, line)
        else:
            self.left_text.insert(tk.END, "Sorry, we don't recognize this passenger. Try a different one.", 'error')

        self.left_text.config(state=tk.DISABLED)

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()


if __name__ == '__main__':
    run()
