from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

def plot():
    fig = Figure(figsize = (5,5), dpi=100)
    y = [i**2 for i in range(101)]
    plot1 = fig.add_subplot(111)
    plot1.plot(y)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

options = ['7 days', '30 days', '1 year']

root = tk.Tk()
root.title('Weather Analysis (CS122 Project)')
root.geometry('800x600')

frame = tk.Frame(root)
entry = tk.Entry(frame)
button = tk.Button(frame, text='Enter')

popup_button = tk.Button(text='Show Current Weather')

dropdown_zoom = tk.Frame(root)
selected = tk.StringVar(value='7 days')
dropdown = tk.OptionMenu(dropdown_zoom, selected, *options)
zoom_in = tk.Button(dropdown_zoom, text='+')
zoom_out = tk.Button(dropdown_zoom, text='-')

save_button = tk.Button(text='Save plot as PNG')

frame.pack()
entry.grid(row=0, column=0)
button.grid(row=0, column=1)

popup_button.pack()

dropdown_zoom.pack()
dropdown.grid(row=0, column=0)
zoom_in.grid(row=0, column=1)
zoom_out.grid(row=0, column=2)

save_button.pack()

plot()

root.mainloop()
