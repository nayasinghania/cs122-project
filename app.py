from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import tkinter.font as tkfont
import os
from cities import save_data, cloud_type
import json
import pandas as pd


def on_close():
    if os.path.exists("weather.csv"):
        os.remove("weather.csv")
    root.destroy()


def submit():
    city = city_var.get()
    save_data(city)


def search_location():
    frame = tk.Frame(root)
    entry = tk.Entry(frame, textvariable=city_var)
    button = tk.Button(frame, text="Enter", command=submit)

    frame.pack()
    entry.grid(row=0, column=0)
    button.grid(row=0, column=1)


def open_popup():
    with open("weather.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    curr = data["current"]
    popup = tk.Toplevel(root)
    popup.geometry("400x300")
    popup.title("Current Weather")
    city = city_var.get()
    label = tk.Label(popup, text="Current Weather in " + city)
    temp = tk.Label(
        popup,
        text=str(curr["temperature_2m"])
        + " degrees and "
        + cloud_type(curr["cloud_cover"]),
    )
    label.pack()
    temp.pack()


def plot():
    fig = Figure(figsize=(5, 5), dpi=100)
    y = [i**2 for i in range(101)]
    plot1 = fig.add_subplot(111)
    plot1.plot(y)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()



options = ["7 days", "30 days", "1 year"]

root = tk.Tk()
root.title("Weather Analysis (CS122 Project)")
root.geometry("800x600")
root.protocol("WM_DELETE_WINDOW", on_close)

city_var = tk.StringVar()

search_location()

popup_button = tk.Button(text="Show Current Weather", command=open_popup)

dropdown_zoom = tk.Frame(root)
selected = tk.StringVar(value="7 days")
dropdown = tk.OptionMenu(dropdown_zoom, selected, *options)
zoom_in = tk.Button(dropdown_zoom, text="+")
zoom_out = tk.Button(dropdown_zoom, text="-")

save_button = tk.Button(text="Save plot as PNG")

popup_button.pack()

dropdown_zoom.pack()
dropdown.grid(row=0, column=0)
zoom_in.grid(row=0, column=1)
zoom_out.grid(row=0, column=2)

save_button.pack()

plot()

root.mainloop()
