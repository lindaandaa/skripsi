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
        self.root.geometry("1000x600")

        # Setup simulation (replaces serial communication with Arduino)
        self.simulate_data = True

        # Navigation Bar
        self.navbar = tk.Menu(root)
        self.root.config(menu=self.navbar)
        self.file_menu = tk.Menu(self.navbar, tearoff=0)
        self.navbar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Exit", command=root.destroy)

        self.save_menu = tk.Menu(self.navbar, tearoff=0)
        self.navbar.add_cascade(label="Save", menu=self.save_menu)
        self.save_menu.add_command(label="Save Data", command=self.save_data)
        self.save_menu.add_command(label="Save Image")

        # COM Manager and Connection Manager
        self.top_frame = ttk.Frame(root)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        self.com_manager_frame = ttk.LabelFrame(self.top_frame, text="Com Manager")
        self.com_manager_frame.pack(side=tk.LEFT, padx=10, pady=10)

        ttk.Label(self.com_manager_frame, text="Available Ports:").grid(row=0, column=0)
        self.com_port_combo = ttk.Combobox(self.com_manager_frame)
        self.com_port_combo.grid(row=0, column=1)
        ttk.Button(self.com_manager_frame, text="Refresh").grid(row=0, column=2)
        ttk.Label(self.com_manager_frame, text="Duration").grid(row=1, column=0)
        self.duration_entry = ttk.Entry(self.com_manager_frame)
        self.duration_entry.grid(row=1, column=1)
        self.baud_rate_combo = ttk.Combobox(self.com_manager_frame, values=["115200"])
        self.baud_rate_combo.grid(row=1, column=2)
        ttk.Button(self.com_manager_frame, text="Disconnect").grid(row=2, columnspan=3)

        self.connection_manager_frame = ttk.LabelFrame(self.top_frame, text="Connection Manager")
        self.connection_manager_frame.pack(side=tk.LEFT, padx=10, pady=10)

        ttk.Label(self.connection_manager_frame, text="Sync Status:").grid(row=0, column=0)
        self.sync_status_label = ttk.Label(self.connection_manager_frame, text="OK")
        self.sync_status_label.grid(row=0, column=1)
        ttk.Label(self.connection_manager_frame, text="Active channels:").grid(row=1, column=0)
        self.active_channels_label = ttk.Label(self.connection_manager_frame, text="4")
        self.active_channels_label.grid(row=1, column=1)
        ttk.Button(self.connection_manager_frame, text="Start").grid(row=2, column=0)
        ttk.Button(self.connection_manager_frame, text="Stop").grid(row=2, column=1)

        ttk.Button(self.top_frame, text="Proses").pack(side=tk.LEFT, padx=10, pady=10)

        # Plot Areas
        self.plot_frame = ttk.Frame(root)
        self.plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(12, 4))
        self.ax1.set_title('EGM Signal 1')
        self.ax1.set_xlabel('Time')
        self.ax1.set_ylabel('Frekuensi')
        self.line1, = self.ax1.plot([], [], lw=2)

        self.ax2.set_title('EGM Signal 2')
        self.ax2.set_xlabel('Time')
        self.ax2.set_ylabel('Frekuensi')
        self.line2, = self.ax2.plot([], [], lw=2)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Explanation and Result Sections
        self.bottom_frame = ttk.Frame(root)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        self.explanation_frame = ttk.LabelFrame(self.bottom_frame, text="Explanation")
        self.explanation_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(self.explanation_frame, text="Gender").grid(row=0, column=0)
        self.gender_entry = ttk.Entry(self.explanation_frame)
        self.gender_entry.grid(row=0, column=1)
        ttk.Label(self.explanation_frame, text="Weight").grid(row=1, column=0)
        self.weight_entry = ttk.Entry(self.explanation_frame)
        self.weight_entry.grid(row=1, column=1)
        ttk.Label(self.explanation_frame, text="Age").grid(row=2, column=0)
        self.age_entry = ttk.Entry(self.explanation_frame)
        self.age_entry.grid(row=2, column=1)

        self.result_frame = ttk.LabelFrame(self.bottom_frame, text="Result")
        self.result_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(self.result_frame, text="Frequency Value:").grid(row=0, column=0)
        self.freq_value_entry = ttk.Entry(self.result_frame)
        self.freq_value_entry.grid(row=0, column=1)
        ttk.Label(self.result_frame, text="Classification:").grid(row=1, column=0)
        self.classification_entry = ttk.Entry(self.result_frame)
        self.classification_entry.grid(row=1, column=1)

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
