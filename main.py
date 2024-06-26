import json
import time
import tkinter as tk


class KeyCounter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Key Counter")
        self.geometry("300x200")
        self.z_count = 0
        self.x_count = 0
        self.timer_running = False
        self.start_time = None
        self.clicks_per_second = []

        self.bpm_label = tk.Label(self, text="", font=("Arial", 12))
        self.bpm_label.pack()

        self.label = tk.Label(self, text="Press 'z' or 'x' to count\nPress Enter to start timer", font=("Arial", 14))
        self.label.pack(pady=20)

        self.z_label = tk.Label(self, text=f"'z' count: {self.z_count}", font=("Arial", 12))
        self.z_label.pack()

        self.x_label = tk.Label(self, text=f"'x' count: {self.x_count}", font=("Arial", 12))
        self.x_label.pack()

        self.total_label = tk.Label(self, text=f'total count: {self.z_count + self.x_count}', font=("Arial", 12, 'bold'))
        self.total_label.pack(pady=10)

        self.bind("<KeyPress>", self.handle_keypress)
        self.bind("<Return>", self.start_timer)

    def handle_keypress(self, event):
        if self.timer_running:
            if event.char == "z":
                self.z_count += 1
                self.z_label.config(text=f"'z' count: {self.z_count}")
            elif event.char == "x":
                self.x_count += 1
                self.x_label.config(text=f"'x' count: {self.x_count}")
            self.total_label.config(text=f"total count: {self.z_count + self.x_count}")

            # Calculate clicks per second
            elapsed_time = time.time() - self.start_time
            clicks_per_second = (self.z_count + self.x_count) / elapsed_time
            self.clicks_per_second.append(clicks_per_second)

    def start_timer(self, event):
        self.reset_counts()
        if not self.timer_running:
            self.timer_running = True
            self.start_time = time.time()
            self.label.config(text="Timer started! Press 'z' or 'x' to count")
            self.after(5000, self.stop_timer)  # 5000 ms = 5 seconds

    def get_current_datetime(self):
        # Return current date and time formatted as "YYYY-MM-DD | HH:MM:SS"
        return time.strftime("%Y-%m-%d | %H:%M:%S", time.localtime())

    def stop_timer(self):
        self.timer_running = False
        self.label.config(text="Timer ended")
        self.total_label.pack()

        # Calculate mean BPM
        mean_clicks_per_second = sum(self.clicks_per_second) / len(self.clicks_per_second)
        bpm = mean_clicks_per_second * 15

        # Prepare data to write to JSON
        data = {
            f"{self.get_current_datetime()}": {
                "z": self.z_count,
                "x": self.x_count,
                "total": self.z_count + self.x_count,
                "BPM": bpm
            }
        }

        # Read existing data from JSON file if it exists
        try:
            with open("countData.json", "r") as file:
                existing_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = {}

        # Update existing data with new data
        existing_data.update(data)

        # Write updated data to JSON file
        with open("countData.json", "w") as file:
            json.dump(existing_data, file, indent=4)  # Write JSON data with indentation for readability

        if bpm >= 1000:
            self.bpm_label.config(text=f"BPM: {bpm:.2f}")
        else:
            self.bpm_label.config(text=f"BPM: {bpm:.2f}")

    def reset_counts(self):
        self.z_count = 0
        self.x_count = 0
        self.z_label.config(text=f"'z' count: {self.z_count}")
        self.x_label.config(text=f"'x' count: {self.x_count}")
        self.total_label.config(text=f"total count: {self.z_count + self.x_count}")


if __name__ == "__main__":
    app = KeyCounter()
    app.mainloop()
