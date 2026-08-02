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
    popup.configure(bg="white")
    city = city_var.get()
    label = tk.Label(
        popup,
        text="Current Weather in " + city,
        font=("Trebuchet MS", 20,"bold italic"),
        bg="lightgrey",
        fg="black",
        pady=5
    )
    temp = tk.Label(
        popup,
        text=str(curr["temperature_2m"])
        + " °F and "
        + cloud_type(curr["cloud_cover"]),
        font=("Segoe UI", 16),
        bg="white",
        fg="black"
    )
    label.pack(fill=tk.X,pady=(0,20))
    temp.pack(pady=20)
