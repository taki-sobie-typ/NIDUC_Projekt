from simulation_frame import SimulationFrame
import tkinter as tk
from tkinter import ttk


def main():
    root = tk.Tk()
    root.title("Shop Simulation Parameters")

    # Define style for notebook and frame
    style = ttk.Style(root)
    style.configure('TNotebook', background='#fff')
    style.configure('TFrame', background='#fff')

    app = SimulationFrame(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()