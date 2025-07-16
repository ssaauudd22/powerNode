import tkinter as tk
import random
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class PowerNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.voltage = 230.0
        self.frequency = 60.0
        self.current = 10.0
        self.status = "OK"

        self.time_data = []
        self.voltage_data = []
        
    def update_readings(self):
        self.voltage = round(random.uniform(180, 260), 2)
        self.frequency = round(random.uniform(58, 62), 2)
        self.current = round(random.uniform(0, 20), 2)

        now = datetime.now()
        self.time_data.append(now)
        self.voltage_data.append(self.voltage)

        if len(self.time_data) > 20:
            self.time_data.pop(0)
            self.voltage_data.pop(0)

    def check_anomaly(self):
        if self.voltage < 210 or self.voltage > 250:
            self.status = "ANOMALY"
        elif self.frequency < 58 or self.frequency > 62:
            self.status = "ANOMALY"
        elif self.current > 12:
            self.status = "ANOMALY"
        else:
            self.status = "OK"

        now = datetime.now()
        time = now.strftime("%A %B %d, %Y %I:%M:%S %p")

        log_line = f"{time} | Node {self.node_id} | V: {self.voltage} | F: {self.frequency} | C: {self.current} | Status: {self.status}\n\n"
        with open("detailed_powernode_log.txt", "a") as file:
            file.write(log_line)

        if self.status == "ANOMALY":
            with open("anomaly_powernode_log.txt", "a") as file:
                file.write(log_line)

def start_gui(node_list):
    root = tk.Tk()
    root.title("Power Grid Simulation")

    label_dict = {}

    for i, node in enumerate(node_list):
        label = tk.Label(root, text="", font=("Arial", 12), width=80, anchor="w")
        label.grid(row=i, column=0, padx=10, pady=5)
        label_dict[node.node_id] = label

    fig, ax = plt.subplots(figsize=(6, 4))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().grid(row=0, column=1, rowspan=len(node_list))

    exit_button = tk.Button(root, text="Exit", command=root.destroy)
    exit_button.grid(row=len(node_list) + 1, column=0, padx=10, pady=10)


    def update_gui():
    # Update each node's readings and status
        for node in node_list:
            node.update_readings()
            node.check_anomaly()

            display = f"Node {node.node_id} | V: {node.voltage} | F: {node.frequency} | I: {node.current} | Status: {node.status}\n\n"
            color = "green" if node.status == "OK" else "red"
            label_dict[node.node_id].config(text=display, fg=color)

        # Plot voltage for all nodes
        ax.clear()
        for node in node_list:
            if node.time_data:  # only plot if there is data
                ax.plot(
                    node.time_data,
                    node.voltage_data,
                    marker='o',
                    label=f"{node.node_id} Voltage"
                )

        ax.set_title("Voltage Over Time")
        ax.set_xlabel("Time")
        ax.set_ylabel("Voltage (V)")
        ax.legend(loc="upper left")
        ax.grid(True)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        fig.autofmt_xdate()
        canvas.draw()

        root.after(1000, update_gui)

    ##def update_gui():
    ##    for node in node_list:
    ##        node.update_readings()
    ##        node.check_anomaly()
##
    ##        display = f"Node {node.node_id} | V: {node.voltage} | F: {node.frequency} | I: {node.current} | Status: {node.status}\n\n"
##
    ##        color = "green" if node.status == "OK" else "red"
    ##        label_dict[node.node_id].config(text=display, fg=color)
##
    ##    node = node_list[0]
    ##    ax.clear()
    ##    ax.plot(node.time_data, node.voltage_data, marker='o', color="blue", label=f"{node.node_id} Voltage")
    ##    ax.set_title("Voltage Over Time (Most Recent Node)")
    ##    ax.set_xlabel("Time")
    ##    ax.set_ylabel("Voltage (V)")
    ##    ax.legend(loc="upper left")
    ##    ax.grid(True)
    ##    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:S'))
    ##    fig.autofmt_xdate()
    ##    canvas.draw()
##
    ##    root.after(1000, update_gui)
##
    update_gui()
    root.mainloop()

def main():
    node_list = []

    print("Welcome to PowerNode Monitor Simulation")
    num_nodes = int(input(f"How many nodes do you want to set up: "))
    
    for i in range(num_nodes):
        node_id = input(f"Name for node {i+1}: ")
        node = PowerNode(node_id)
        node_list.append(node)

    start_gui(node_list)

if __name__ == "__main__":
    main()