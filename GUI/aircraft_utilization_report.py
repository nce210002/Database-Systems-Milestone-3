import tkinter as tk
from tkinter import messagebox
import sqlite3
import os


def run():
    root = tk.Tk()
    app = AircraftUtilizationReport(root)
    root.mainloop()


class AircraftUtilizationReport:
    def __init__(self, root):
        self.root = root
        self.root.title("Aircraft Utilization Report")
        self.root.geometry("760x520")

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
        # Minimal tables: AIRPLANE, AIRPLANE_TYPE, LEG_INSTANCE
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS AIRPLANE_TYPE (
                Type_name TEXT PRIMARY KEY,
                Total_seats INTEGER
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS AIRPLANE (
                Airplane_id INTEGER PRIMARY KEY,
                Type_name TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS LEG_INSTANCE (
                Flight_no TEXT,
                Date TEXT,
                Leg_no INTEGER,
                Airplane_id INTEGER,
                Available_seats INTEGER
            )
        ''')

        # sample data
        sample_types = [
            ('Boeing737', 180),
            ('A320', 150),
        ]
        sample_planes = [
            (1, 'Boeing737'),
            (2, 'A320'),
            (3, 'Boeing737'),
        ]
        sample_instances = [
            ('AA100', '2026-05-01', 1, 1, 180),
            ('AA101', '2026-05-02', 1, 1, 178),
            ('UA200', '2026-05-03', 1, 2, 150),
            ('DL300', '2026-05-04', 1, 3, 170),
            ('DL301', '2026-05-05', 1, 3, 168),
        ]

        for t in sample_types:
            try:
                self.cursor.execute('INSERT INTO AIRPLANE_TYPE VALUES (?, ?)', t)
            except sqlite3.IntegrityError:
                pass
        for p in sample_planes:
            try:
                self.cursor.execute('INSERT INTO AIRPLANE VALUES (?, ?)', p)
            except sqlite3.IntegrityError:
                pass
        for inst in sample_instances:
            try:
                self.cursor.execute('INSERT INTO LEG_INSTANCE VALUES (?, ?, ?, ?, ?)', inst)
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

        title = tk.Label(header, text="Aircraft Utilization Report", font=('Arial', 16, 'bold'), bg='#f0f0f0')
        title.pack(side=tk.LEFT, padx=20)

        # date range inputs
        controls = tk.Frame(self.root)
        controls.pack(fill=tk.X, padx=20, pady=12)

        from_label = tk.Label(controls, text="From (YYYY-MM-DD):", font=('Arial', 11))
        from_label.grid(row=0, column=0, sticky='w')
        self.from_entry = tk.Entry(controls, font=('Arial', 11), width=18)
        self.from_entry.grid(row=0, column=1, padx=8)

        to_label = tk.Label(controls, text="To (YYYY-MM-DD):", font=('Arial', 11))
        to_label.grid(row=0, column=2, sticky='w')
        self.to_entry = tk.Entry(controls, font=('Arial', 11), width=18)
        self.to_entry.grid(row=0, column=3, padx=8)

        run_btn = tk.Button(controls, text="Generate", command=self.generate_report, font=('Arial', 11), bg='#4CAF50', fg='white')
        run_btn.grid(row=0, column=4, padx=8)

        # results area
        content = tk.Frame(self.root)
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=8)

        left = tk.Frame(content, relief=tk.SUNKEN, borderwidth=1)
        left.pack(fill=tk.BOTH, expand=True)
        left_title = tk.Label(left, text="Report", font=('Arial', 12, 'bold'))
        left_title.pack(anchor='nw', padx=8, pady=8)
        self.left_text = tk.Text(left, font=('Courier', 10), state=tk.DISABLED)
        self.left_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0,8))
        # tag for error messages (red)
        self.left_text.tag_configure('error', foreground='red')

    def generate_report(self):
        start = self.from_entry.get().strip()
        end = self.to_entry.get().strip()

        if not start or not end:
            messagebox.showwarning("Input Error", "Please enter both start and end dates")
            return

        # Query: count LEG_INSTANCE rows per Airplane_id in date range
        self.cursor.execute('''
            SELECT li.Airplane_id, a.Type_name, COUNT(*) as total_flights
            FROM LEG_INSTANCE li LEFT JOIN AIRPLANE a ON li.Airplane_id = a.Airplane_id
            WHERE Date BETWEEN ? AND ?
            GROUP BY li.Airplane_id, a.Type_name
            ORDER BY total_flights DESC
        ''', (start, end))
        rows = self.cursor.fetchall()

        self.left_text.config(state=tk.NORMAL)
        self.left_text.delete(1.0, tk.END)

        if rows:
            self.left_text.insert(tk.END, "Registration# | Aircraft Type | Total Flights\n")
            self.left_text.insert(tk.END, "-" * 60 + "\n")
            for airplane_id, type_name, total in rows:
                reg = str(airplane_id)
                typ = type_name or 'Unknown'
                self.left_text.insert(tk.END, f"{reg:13} | {typ:13} | {total:13}\n")
        else:
            self.left_text.insert(tk.END, "No data found for the specified period.", 'error')

        self.left_text.config(state=tk.DISABLED)

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()


if __name__ == '__main__':
    run()
