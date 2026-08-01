import csv
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator

PERIOD_DAYS = {"7 days": 7, "30 days": 30, "1 year": 365}


def read_weather_data():
    dates, temp_min, temp_max = [], [], []
    with open("weather.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            dates.append(row["date"])
            temp_min.append(float(row["temp_min"]))
            temp_max.append(float(row["temp_max"]))
    return dates, temp_min, temp_max


def plot(root, canvas, period):
    if not os.path.exists("weather.csv"):
        return canvas

    dates, temp_min, temp_max = read_weather_data()
    days = PERIOD_DAYS[period]
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
        label.set_horizontalalignment("right")
    plot1.legend()
    plot1.grid()
    fig.tight_layout()

    if canvas is not None:
        canvas.get_tk_widget().destroy()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()
    return canvas
