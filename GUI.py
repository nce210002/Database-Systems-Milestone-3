import tkinter as tk

root = tk.Tk()
root.title("Airport System")
root.geometry("550x200")  # Default window size

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
searchflight_button = tk.Button(root, text="Search Flight 🔍✈️", width=18, height=3, command=root.destroy)
searchflight_button.pack(side=tk.LEFT, padx=5, pady=5)

# Search Trip Button
searchtrip_button = tk.Button(root, text="Search Trip 🔍📍", width=18, height=3, command=root.destroy)
searchtrip_button.pack(side=tk.LEFT, padx=5, pady=5)

# Seat Avaulability Button
seatavailability_button = tk.Button(root, text="Seat Availability 💺", width=18, height=3, command=root.destroy)
seatavailability_button.pack(side=tk.LEFT, padx=5, pady=5)


"""Middle Row"""
# Passenger Itinerary Button
passengeritinerary_button = tk.Button(root, text="Passenger Itinerary 👤", width=18, height=3, command=root.destroy)
passengeritinerary_button.pack(side=tk.BOTTOM)

root.mainloop()