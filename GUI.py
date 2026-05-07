import tkinter as tk

root = tk.Tk()
root.title("Airport System")
root.geometry("400x200")  # Default window size

# Intro GUI page
label = tk.Label(root, text="Welcome to the Airport System! Select an activity.")
label.pack()

## Buttons for different activities
button = tk.Button(root, text="Search Flight", width=25, command=root.destroy)
button.pack()

root.mainloop()