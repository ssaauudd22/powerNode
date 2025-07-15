import tkinter as tk
import random

root = tk.Tk()

class PowerNode:
    #constructor
    def __init__(self, node_id):
        self.node_id = node_id
        self.voltage = 230.0
        self.frequency = 60.0
        self.current = 10.0
        self.status = "Ok"

    #methods
    def update_readings(self):
        #randomly change voltage, frequency, and current
        self.voltage = round(random.uniform(180, 260), 2)
        self.frequency = round(random.uniform(58, 62), 2)
        self.current = round(random.uniform(0, 20), 2)

    def check_anomaly(self):
        #check if there is something wrong with a node
        if self.voltage < 210 or self.voltage > 250:
            self.status = "ANOMALY"
        elif self.frequency < 58 or self.frequency > 62:
            self.status = "ANOMALY"
        elif self.current > 12:
            self.status = "ANOMALY"
        else:
            self.status = "Ok"
        
        print(f"Node {self.node_id} status: {self.status}")


root.mainloop()