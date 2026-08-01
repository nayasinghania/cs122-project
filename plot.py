import csv
import os
from matplotlib import axes
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator


PERIOD_DAYS = {"7 days": 7, "30 days": 30, "1 year": 365}

current_ax = None
current_fig = None


def read_weather_data():
    dates, temp_min, temp_max = [], [], []
    with open("weather.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            dates.append(row["date"])
            temp_min.append(float(row["temp_min"]))
            temp_max.append(float(row["temp_max"]))
    return dates, temp_min, temp_max


def calculate_trend(dates, temps):
    '''
    Calculates the trend line for the given dates and temperatures using a quadratic polynomial fit.
    '''
    coeffs = np.polyfit(range(len(dates)),temps,2)
    return coeffs


def zoom_in():
    global current_ax, current_fig
    if current_ax is None:
        return

    # Get current limits
    x_min, x_max = current_ax.get_xlim()
    y_min, y_max = current_ax.get_ylim()

    # Calculate center
    x_center = (x_min + x_max) / 2
    y_center = (y_min + y_max) / 2

    # Calculate new ranges (zoome in by 10%)
    zoom_factor = 0.9
    x_range = (x_max - x_min) * zoom_factor / 2
    y_range = (y_max - y_min) * zoom_factor / 2

    # Set new limits
    current_ax.set_xlim(x_center - x_range, x_center + x_range)
    current_ax.set_ylim(y_center - y_range, y_center + y_range)

    # Redraw the canvas
    current_fig.canvas.draw()


def zoom_out():
    global current_ax, current_fig
    if current_ax is None:
        return

    # Get current limits
    x_min, x_max = current_ax.get_xlim()
    y_min, y_max = current_ax.get_ylim()

    # Calculate center
    x_center = (x_min + x_max) / 2
    y_center = (y_min + y_max) / 2

    # Calculate new ranges (zoom out by 10%)
    zoom_factor = 1.1
    x_range = (x_max - x_min) * zoom_factor / 2
    y_range = (y_max - y_min) * zoom_factor / 2

    # Set new limits
    current_ax.set_xlim(x_center - x_range, x_center + x_range)
    current_ax.set_ylim(y_center - y_range, y_center + y_range)

    # Redraw the canvas
    current_fig.canvas.draw()


def plot(root, canvas, period):
    global current_ax, current_fig

    if not os.path.exists("weather.csv"):
        return canvas

    dates, temp_min, temp_max = read_weather_data()
    days = PERIOD_DAYS[period]
    dates = dates[-days:]
    temp_min = temp_min[-days:]
    temp_max = temp_max[-days:]

    fig = Figure(figsize=(12, 8), dpi=100)
    plot1 = fig.add_subplot(111)
    plot1.plot(dates, temp_max, label="High", color="red", linewidth=2)
    plot1.plot(dates, temp_min, label="Low", color="blue", linewidth=2)

    max_coeffs = calculate_trend(dates, temp_max)
    min_coeffs = calculate_trend(dates, temp_min)
    trend_line_max = np.poly1d(max_coeffs)
    trend_line_min = np.poly1d(min_coeffs)
    x = np.linspace(0, len(dates) - 1, len(dates))
    plot1.plot(dates, trend_line_max(x), label="High Trend", color="lightcoral", linewidth=2,linestyle='--')
    plot1.plot(dates, trend_line_min(x), label="Low Trend", color="lightblue", linewidth=2, linestyle='--')

    plot1.set_xlabel("Date")
    plot1.set_ylabel("Temperature (°F)")
    plot1.xaxis.set_major_locator(MaxNLocator(10))
    for label in plot1.get_xticklabels():
        label.set_rotation(45)
        label.set_horizontalalignment("right")
    plot1.legend()
    plot1.grid()
    fig.tight_layout()

    # Store global references for zoom functions
    current_ax = plot1
    current_fig = fig

    if canvas is not None:
        canvas.get_tk_widget().destroy()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(padx=10, pady=10)
    return canvas
