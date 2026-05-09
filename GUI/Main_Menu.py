import tkinter as tk

root = tk.Tk()
root.title("Airport System")
root.geometry("550x250")  # Default window size

# Intro GUI page
label = tk.Label(root, text="Welcome to the Airport System! Select an activity.")
label.pack()

'''List of Buttons for the GUI'''
# Organize button layout
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Top Row - 3 buttons
top_frame = tk.Frame(button_frame)
top_frame.pack()

# Search Flight Button
searchflight_button = tk.Button(top_frame, text="Search Flight 🔍✈️", width=18, height=3, command=root.destroy)
searchflight_button.pack(side=tk.LEFT, padx=5, pady=5)

# Search Trip Button
searchtrip_button = tk.Button(top_frame, text="Search Trip 🔍📍", width=18, height=3, command=root.destroy)
searchtrip_button.pack(side=tk.LEFT, padx=5, pady=5)

# Seat Availability Button
seatavailability_button = tk.Button(top_frame, text="Seat Availability 💺", width=18, height=3, command=root.destroy)
seatavailability_button.pack(side=tk.LEFT, padx=5, pady=5)


"""Middle Row"""
# Middle row frame
middle_frame = tk.Frame(button_frame)
middle_frame.pack()

# Passenger Itinerary Button
passengeritinerary_button = tk.Button(middle_frame, text="Passenger Itinerary 👤", width=25, height=3, command=root.destroy)
passengeritinerary_button.pack(side=tk.LEFT, padx=5, pady=5)

# Aircraft Utilization Report Button
aircraftutilizationreport_button = tk.Button(middle_frame, text="Aircraft Utilization Report 📊", width=25, height=3, command=root.destroy)
aircraftutilizationreport_button.pack(side=tk.LEFT, padx=5, pady=5)


# Exit Button
exit_button = tk.Button(root, text="Exit 👋", width=18, height=3, command=root.destroy)
exit_button.pack(pady=10)

root.mainloop()