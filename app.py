import tkinter as tk
import tkinter.font as tkfont
import os

from numpy import pad
from cities import save_data
from plot import plot
from popup import open_popup


def on_close():
    if os.path.exists("weather.csv"):
        os.remove("weather.csv")
    if os.path.exists("weather.json"):
        os.remove("weather.json")
    root.destroy()


def update_plot():
    global canvas
    canvas = plot(root, canvas, selected.get())


def submit():
    city = city_var.get()
    save_data(city)
    update_plot()


def search_location():
    frame = tk.Frame(root)
    entry = tk.Entry(
        frame,
        textvariable=city_var,
        font=("Arial", 14),
        bg="lightgrey",
        fg="black"
    )
    button = tk.Button(
        frame,
        text="Enter",
        command=submit,
        font=("Arial", 14),
        bg="lightgrey",
        fg="black"
    )

    frame.pack(pady=(10,5))
    entry.grid(row=0, column=0)
    button.grid(row=0, column=1)


options = ["7 days", "30 days", "1 year"]

root = tk.Tk()
root.title("Weather Analysis (CS122 Project)")
root.geometry("1200x800")
root.configure(bg='white')
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.protocol("WM_DELETE_WINDOW", on_close)

header = tk.Label(
    root,
    text="Weather Analysis",
    font=("Arial",20,"bold"),
    bg="lightgrey",
    fg="black",
    pady=5
)
header.pack(fill=tk.X, pady=(0,10))

city_var = tk.StringVar()

search_location()

popup_button = tk.Button(
    text="Show Current Weather",
    font=("Arial", 14),
    command=lambda: open_popup(root, city_var),
    bg="lightgrey",
    fg="black",
    width=20
)

canvas = None

dropdown_zoom = tk.Frame(root)
selected = tk.StringVar(value="7 days")
selected.trace_add("write", lambda *args: update_plot())
dropdown = tk.OptionMenu(dropdown_zoom, selected, *options)
dropdown.config(
    font=("Arial", 14),
    bg="lightgrey",
    fg="black"
)
zoom_in = tk.Button(
    dropdown_zoom,
    text="+",
    font=("Arial", 14),
    bg="lightgrey",
    fg="black"
)
zoom_out = tk.Button(
    dropdown_zoom,
    text="-",
    font=("Arial", 14),
    bg="lightgrey",
    fg="black"
)

save_button = tk.Button(
    text="Save plot as PNG",
    font=("Arial", 14),
    bg="lightgrey",
    fg="black"
)

popup_button.pack(pady=5)

dropdown_zoom.pack(pady=5)
dropdown.grid(row=0, column=0)
zoom_in.grid(row=0, column=1)
zoom_out.grid(row=0, column=2)

save_button.pack(pady=5)

update_plot()

root.mainloop()
