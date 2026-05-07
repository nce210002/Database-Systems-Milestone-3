import tkinter as tk

root = tk.Tk()



var1 = tk.IntVar()
var2 = tk.IntVar()

tk.Checkbutton(root, text="Male", variable=var1).grid(row=1, sticky=tk.W)
tk.Checkbutton(root, text="Female", variable=var2).grid(row=2, sticky=tk.W)
root.mainloop()