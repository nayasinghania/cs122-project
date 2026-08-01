import tkinter as tk
import os
from cities import save_data
from plot import plot, zoom_in, zoom_out, save_plot
from popup import open_popup


original_limits = None


def on_close():
    if os.path.exists("weather.csv"):
        os.remove("weather.csv")
    if os.path.exists("weather.json"):
        os.remove("weather.json")
    root.destroy()


def update_plot():
    global canvas, original_limits
    canvas = plot(root, canvas, selected.get())
    # Store original limits after plot is created
    if canvas and hasattr(canvas,'figure'):
        ax = canvas.figure.axes[0]
        original_limits = (ax.get_xlim(), ax.get_ylim())


def reset_zoom():
    global canvas, original_limits
    if canvas and original_limits:
        ax = canvas.figure.axes[0]
        xlim, ylim = original_limits
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        canvas.draw()


def submit():
    city = city_var.get()
    save_data(city)
    update_plot()


def search_location():
    frame = tk.Frame(root)
    entry = tk.Entry(
        frame,
        textvariable=city_var,
        font=("Arial", 12),
        bg="white",
        fg="black"
    )
    button = tk.Button(
        frame,
        text="Enter",
        command=submit,
        font=("Arial", 12, "bold"),
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
    font=("Arial", 12),
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
    font=("Arial", 12),
    bg="lightgrey",
    fg="black"
)
zoom_in_button = tk.Button(
    dropdown_zoom,
    text="+",
    font=("Arial", 12),
    bg="lightgrey",
    fg="black",
    command=zoom_in
)
zoom_out_button = tk.Button(
    dropdown_zoom,
    text="-",
    font=("Arial", 12),
    bg="lightgrey",
    fg="black",
    command=zoom_out
)
reset_zoom_button = tk.Button(
    dropdown_zoom,
    text="Reset",
    font=("Arial",10),
    bg="lightgrey",
    fg="black",
    command=reset_zoom
)
save_button = tk.Button(
    text="Save plot as PNG",
    font=("Arial", 12),
    bg="lightgrey",
    fg="black",
    command=save_plot
)

popup_button.pack(pady=5)

dropdown_zoom.pack(pady=5)
dropdown.grid(row=0, column=0)
zoom_in_button.grid(row=0, column=1,padx=2)
zoom_out_button.grid(row=0, column=2,padx=2)
reset_zoom_button.grid(row=0,column=3,padx=2)

save_button.pack(pady=5)

update_plot()

root.mainloop()
