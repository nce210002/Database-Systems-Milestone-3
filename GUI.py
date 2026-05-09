import tkinter as tk

root = tk.Tk()
root.title("Airport System")
root.geometry("400x200")  # Default window size

# Intro GUI page
label = tk.Label(root, text="Welcome to the Airport System! Select an activity.")
label.pack()

'''List of Buttons for the GUI'''
# Search Flight Button
searchflight_button = tk.Button(root, text="Search Flight 🔍✈️", width=25, command=root.destroy)
searchflight_button.pack(side=tk.LEFT)

# Search Trip Button
searchtrip_button = tk.Button(root, text="Search Trip", width=25, command=root.destroy)
searchtrip_button.pack(side=tk.LEFT)

root.mainloop()