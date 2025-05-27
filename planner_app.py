import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

resources = ["Supplies", "Components", "Fuel", "Electronics", "Rare Material", "ManPower", "Money"]

class ResourcePlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Resource Planner")

        self.entries = {}
        self.costs = {}
        self.production = {}

        # Instruction text
        tk.Label(root, text="Only fill in applicable resource fields. Leave others blank.",
                 font=('Arial', 10), fg='gray').grid(row=0, column=0, columnspan=4, pady=(5, 10))

        # Table headers
        tk.Label(root, text="Resource").grid(row=1, column=0)
        tk.Label(root, text="Current").grid(row=1, column=1)
        tk.Label(root, text="Hourly Production").grid(row=1, column=2)
        tk.Label(root, text="Cost per Unit").grid(row=1, column=3)

        # Entry rows
        for i, res in enumerate(resources):
            tk.Label(root, text=res).grid(row=i+2, column=0)

            self.entries[res] = tk.Entry(root, width=10)
            self.entries[res].grid(row=i+2, column=1)

            self.production[res] = tk.Entry(root, width=10)
            self.production[res].grid(row=i+2, column=2)

            self.costs[res] = tk.Entry(root, width=10)
            self.costs[res].grid(row=i+2, column=3)

        # Calculate button
        self.calc_btn = tk.Button(root, text="Calculate Time", command=self.calculate_time)
        self.calc_btn.grid(row=len(resources)+3, column=0, columnspan=2, pady=10)

        # Output result
        self.result_label = tk.Label(root, text="", font=('Arial', 12), justify="left")
        self.result_label.grid(row=len(resources)+4, column=0, columnspan=4)

    def calculate_time(self):
        max_time = 0.0
        for res in resources:
            try:
                current = float(self.entries[res].get() or 0)
                prod = float(self.production[res].get() or 0)
                cost = float(self.costs[res].get() or 0)

                if cost > current:
                    needed = cost - current
                    if prod > 0:
                        time_needed = needed / prod
                        max_time = max(max_time, time_needed)
                    else:
                        max_time = float('inf')  # Cannot produce
            except ValueError:
                continue

        if max_time == float('inf'):
            self.result_label.config(text="Some resources cannot be produced — infinite wait.")
        else:
            hrs = int(max_time)
            mins = int((max_time - hrs) * 60)
            eta = datetime.now() + timedelta(hours=max_time)
            eta_str = eta.strftime("%b %d, %I:%M %p").lstrip('0')
            self.result_label.config(
                text=f"Time until unit affordable: {hrs}h {mins}m\nAvailable at: {eta_str}"
            )

# Launch GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = ResourcePlanner(root)
    root.mainloop()
