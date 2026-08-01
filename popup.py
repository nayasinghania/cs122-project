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
    popup.configure(bg="lightgrey")
    city = city_var.get()
    label = tk.Label(
        popup,
        text="Current Weather in " + city,
        font=("Arial", 20,"bold"),
        bg="lightgrey",
        fg="black"
    )
    temp = tk.Label(
        popup,
        text=str(curr["temperature_2m"])
        + " degrees and "
        + cloud_type(curr["cloud_cover"]),
        font=("Arial", 16),
        bg="lightgrey",
        fg="black"
    )
    label.pack(pady=20)
    temp.pack(pady=20)
