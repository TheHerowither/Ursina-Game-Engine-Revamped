import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext as sc
import editor_compiler as ec


print("Initializing editor")
#Initialization step
edapp = tk.Tk()
edapp.iconbitmap("IMG\\logo.ico")
edapp.title("Behavioral editor")
edapp.geometry("1080x720")
print("initialized app:", type(edapp))

codewin = sc.ScrolledText(edapp, width = 500, height = 100)
codewin.grid(column = 0)
codewin.pack()
print("initialized code window:", type(codewin))



print("initialized editor")
#Code for editor
def saveE(event):
    import tkinter as tk
    from tkinter import ttk
    from tkinter import scrolledtext as sc
    import editor_compiler as ec

    
    global edapp, codewin

    if name == "":
        edapp.destroy()
    else:
        with open(f"projects/{name}/{name}.ugerc", "w") as f:
            f.write(codewin.get("1.0", tk.END))
        with open("temp.tmp", "w") as f:
            f.write(name)
    #with open("")
edapp.bind("<Control-s>", saveE)
edapp.mainloop()
#save()
