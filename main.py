import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import os
import pandas as pd
from datetime import datetime
from collections import deque
import random 

class EGM_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitoring Sinyal Elektromiografi pada Otot Manusia")

        # Setup simulation (replaces serial communication with Arduino)
        self.simulate_data = True

        self.navbar = tk.Menu(root)
        self.root.config(menu=self.navbar)

        # Menu "File"
        self.file_menu = tk.Menu(self.navbar, tearoff=0)
        self.navbar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Exit", command=root.destroy)

        # Menu "Save"
        self.save_menu = tk.Menu(self.navbar, tearoff=0)
        self.navbar.add_cascade(label="Save", menu=self.save_menu)
        self.save_menu.add_command(label="Save Data", command=self.save_data)
        self.save_menu.add_command(label="Save Image", command=self.save_image)

        # Footer Menu
        self.footer_frame = ttk.Frame(root)
        self.footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.result_label = ttk.Label(self.footer_frame, text="Status: Normal/Tidak Lelah/Kelelahan", anchor="e")
        self.result_label.pack(side=tk.BOTTOM, padx=550)

        self.status_label = ttk.Label(root, text="Frekuensi: ", anchor="w", font=("Helvetica", 9))
        self.status_label.pack(side=tk.BOTTOM, padx=300)

        # Create the plot
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(12, 4))
        self.ax1.set_title('EGM Signal 1')
        self.ax1.set_xlabel('Time')
        self.ax1.set_ylabel('Frekuensi')
        self.line1, = self.ax1.plot([], [], lw=2)

        # Create the figure and axes for the second plot
        self.ax2.set_title('EGM Signal 2')
        self.ax2.set_xlabel('Time')
        self.ax2.set_ylabel('Frekuensi')
        self.line2, = self.ax2.plot([], [], lw=2)

        # Create the canvas for both plots
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Initialize data deque for both plots
        self.data1 = deque(maxlen=1000)
        self.data2 = deque(maxlen=1000)

        self.animation()

        # Start the periodic save function
        self.save_interval_ms = 3 * 60 * 1000  # 3 minutes in milliseconds
        self.periodic_save()

    def animation(self):
        def update_plot():
            if self.simulate_data:
                # Generate simulated data
                value = random.uniform(0, 10)
            else:
                # Read data from serial (uncomment this part if you have actual serial data)
                # data = self.serial_port.readline().decode('ascii').strip()
                # if data:
                #     value = float(data)
                pass

            # Process data
            self.data1.append(value)
            self.data2.append(value * random.randint(0, 9))
            self.line1.set_data(range(len(self.data1)), self.data1)
            self.line2.set_data(range(len(self.data2)), self.data2)
            self.ax1.relim()
            self.ax1.autoscale_view()
            self.ax2.relim()
            self.ax2.autoscale_view()
            self.canvas.draw()
            self.canvas.flush_events()

            # Call this function again after 200ms
            self.root.after(200, update_plot)

        # Call the update_plot function initially
        update_plot()


    def save_image(self):
        # Ensure the "record" directory exists
        os.makedirs("record", exist_ok=True)

        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create the filename with the timestamp
        filename = f"record/plot_{timestamp}.png"

        # Save the plot as an image
        self.fig.savefig(filename)
        print(f"Image saved to {filename}")
        
    def save_data(self):
        # Ensure the "record" directory exists
        os.makedirs("record", exist_ok=True)

        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create the filename with the timestamp
        filename = f"record/data_{timestamp}.csv"

        # Combine data1 and data2 into a DataFrame
        df = pd.DataFrame({
            'Time': range(len(self.data1)),
            'EGM Signal 1': list(self.data1),
            'EGM Signal 2': list(self.data2)
        })

        # Save the DataFrame to a CSV file
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

    def periodic_save(self):
        # Save data to CSV
        self.save_data()

        # Schedule the next save after the specified interval
        self.root.after(self.save_interval_ms, self.periodic_save)

if __name__ == "__main__":
    root = tk.Tk()
    app = EGM_GUI(root)
    root.mainloop()
