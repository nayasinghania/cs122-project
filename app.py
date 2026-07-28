from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator
import tkinter as tk
import tkinter.font as tkfont
import os
import csv
from cities import save_data, cloud_type
import json

PERIOD_DAYS = {"7 days": 7, "30 days": 30, "1 year": 365}


def on_close():
    if os.path.exists("weather.csv"):
        os.remove("weather.csv")
    root.destroy()


def submit():
    city = city_var.get()
    save_data(city)
    plot()


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


def read_weather_data():
    dates, temp_min, temp_max = [], [], []
    with open("weather.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            dates.append(row["date"])
            temp_min.append(float(row["temp_min"]))
            temp_max.append(float(row["temp_max"]))
    return dates, temp_min, temp_max


def plot():
    global canvas

    if not os.path.exists("weather.csv"):
        return

    dates, temp_min, temp_max = read_weather_data()
    days = PERIOD_DAYS[selected.get()]
    dates = dates[-days:]
    temp_min = temp_min[-days:]
    temp_max = temp_max[-days:]

    fig = Figure(figsize=(12, 8), dpi=100)
    plot1 = fig.add_subplot(111)
    plot1.plot(dates, temp_max, label="High")
    plot1.plot(dates, temp_min, label="Low")
    plot1.set_xlabel("Date")
    plot1.set_ylabel("Temperature (°F)")
    plot1.xaxis.set_major_locator(MaxNLocator(10))
    for label in plot1.get_xticklabels():
        label.set_rotation(45)
        label.set_ha("right")
    plot1.legend()
    fig.tight_layout()

    if canvas is not None:
        canvas.get_tk_widget().destroy()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()



options = ["7 days", "30 days", "1 year"]

root = tk.Tk()
root.title("Weather Analysis (CS122 Project)")
root.geometry("1200x800")
root.protocol("WM_DELETE_WINDOW", on_close)

city_var = tk.StringVar()

search_location()

popup_button = tk.Button(text="Show Current Weather", command=open_popup)

canvas = None

dropdown_zoom = tk.Frame(root)
selected = tk.StringVar(value="7 days")
selected.trace_add("write", lambda *args: plot())
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
