import tkinter as tk

def packing():
    window = tk.Tk()
    entry = tk.Entry(fg="black", bg="#D3D3D3") #HTML colours allowed
    label = tk.Label(text="Hello, Tkinter", foreground="black", background="white")
    label.pack() ## pack label into window
    entry.pack()
    window.mainloop() ## run tk event loop

def frameBorderEffects():
    border_effects = {
        "flat": tk.FLAT,
        "sunken": tk.SUNKEN,
        "raised": tk.RAISED,
        "groove": tk.GROOVE,
        "ridge": tk.RIDGE,
    }

    window = tk.Tk()

    for relief_name, relief in border_effects.items():
        frame = tk.Frame(master=window, relief=relief, borderwidth=5)
        frame.pack(side=tk.LEFT)
        label = tk.Label(master=frame, text=relief_name)
        label.pack()

    window.mainloop()

if __name__ == "__main__":
    frameBorderEffects()
