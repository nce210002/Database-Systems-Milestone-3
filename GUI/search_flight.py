import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def run():
    """Main function to run the Flight Search GUI"""
    root = tk.Tk()
    app = FlightSearchApp(root)
    root.mainloop()

class FlightSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Search")
        self.root.geometry("600x500")
        
        # Database connection
        self.conn = sqlite3.connect(':memory:')  # Using in-memory DB for demo
        self.cursor = self.conn.cursor()
        self.setup_database()
        
        # Create GUI
        self.create_widgets()
    
    def setup_database(self):
        """Create sample FLIGHT table with test data"""
        self.cursor.execute('''
            CREATE TABLE FLIGHT (
                Number TEXT PRIMARY KEY,
                Origin TEXT,
                Destination TEXT,
                DepartureTime TEXT,
                ArrivalTime TEXT,
                Status TEXT
            )
        ''')
        
        # Insert sample data
        sample_flights = [
            ('AA101', 'New York', 'Los Angeles', '08:00', '11:30', 'On Time'),
            ('UA202', 'Chicago', 'Denver', '10:15', '11:45', 'Boarding'),
            ('DL303', 'Atlanta', 'Miami', '14:00', '15:30', 'Delayed'),
            ('SW404', 'Dallas', 'Houston', '16:30', '17:45', 'On Time'),
        ]
        
        self.cursor.executemany(
            'INSERT INTO FLIGHT VALUES (?, ?, ?, ?, ?, ?)',
            sample_flights
        )
        self.conn.commit()
    
    def create_widgets(self):
        """Create the GUI layout"""
        # Header frame
        header_frame = tk.Frame(self.root, bg='#f0f0f0', height=60)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Back button
        def go_back():
            self.root.destroy()
            try:
                import Main_Menu as mm
            except Exception as e:
                messagebox.showerror("Error", f"Could not open main menu: {e}")
                return
            # If Main_Menu exposes a run() function, call it to start the menu.
            if hasattr(mm, 'run'):
                try:
                    mm.run()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to open main menu: {e}")

        back_btn = tk.Button(
            header_frame,
            text="← Back",
            command=go_back,
            font=('Arial', 10),
            bg='white',
            relief=tk.RAISED,
            width=10
        )
        back_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="Search Flight",
            font=('Arial', 16, 'bold'),
            bg='#f0f0f0'
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Main content frame
        content_frame = tk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Input section
        input_frame = tk.Frame(content_frame)
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Input label
        input_label = tk.Label(
            input_frame,
            text="Enter flight number:",
            font=('Arial', 11),
            anchor='w'
        )
        input_label.pack(fill=tk.X, pady=(0, 5))
        
        # Text entry box
        self.flight_entry = tk.Entry(
            input_frame,
            font=('Arial', 12),
            width=30
        )
        self.flight_entry.pack(fill=tk.X, pady=(0, 10))
        self.flight_entry.bind('<Return>', lambda e: self.search_flight())
        
        # Search button
        search_btn = tk.Button(
            input_frame,
            text="Search",
            command=self.search_flight,
            font=('Arial', 11),
            bg='#4CAF50',
            fg='white',
            padx=20,
            pady=8
        )
        search_btn.pack(anchor='w')
        
        # Results section
        results_label = tk.Label(
            content_frame,
            text="Flight Info:",
            font=('Arial', 11, 'bold'),
            anchor='w'
        )
        results_label.pack(fill=tk.X, pady=(20, 10))
        
        # Results frame with scrollbar
        results_frame = tk.Frame(content_frame, relief=tk.SUNKEN, borderwidth=1)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(results_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Text widget for results
        self.results_text = tk.Text(
            results_frame,
            font=('Courier', 10),
            height=15,
            yscrollcommand=scrollbar.set,
            state=tk.DISABLED
        )
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.results_text.yview)
    
    def search_flight(self):
        """Search for flight and display results"""
        flight_no = self.flight_entry.get().strip().upper()
        
        if not flight_no:
            messagebox.showwarning("Input Error", "Please enter a flight number")
            return
        
        try:
            self.cursor.execute(
                "SELECT * FROM FLIGHT WHERE Number=?",
                (flight_no,)
            )
            result = self.cursor.fetchall()
            
            # Update results text widget
            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete(1.0, tk.END)
            
            if result:
                # Display column headers
                headers = ['Number', 'Origin', 'Destination', 'Departure', 'Arrival', 'Status']
                header_line = " | ".join(f"{h:15}" for h in headers)
                separator = "-" * len(header_line)
                
                self.results_text.insert(tk.END, header_line + "\n")
                self.results_text.insert(tk.END, separator + "\n\n")
                
                # Display flight data
                for row in result:
                    row_line = " | ".join(f"{str(val):15}" for val in row)
                    self.results_text.insert(tk.END, row_line + "\n")
            else:
                self.results_text.insert(
                    tk.END,
                    f"⚠ Flight number not available\n\n"
                    f"Try again with a valid flight number.\n\n"
                    f"Available flights: AA101, UA202, DL303, SW404"
                )
            
            self.results_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")
    
    def __del__(self):
        """Close database connection"""
        if hasattr(self, 'conn'):
            self.conn.close()


if __name__ == "__main__":
    run()