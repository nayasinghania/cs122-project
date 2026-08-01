import tkinter as tk
import json
from cities import cloud_type


def open_popup(root, city_var):
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
