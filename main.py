import tkinter as tk


class KeyCounter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Key Counter")
        self.geometry("300x200")
        self.z_count = 0
        self.x_count = 0
        self.timer_running = False

        self.label = tk.Label(self, text="Press 'z' or 'x' to count\nPress Enter to start timer", font=("Arial", 14))
        self.label.pack(pady=20)

        self.z_label = tk.Label(self, text=f"'z' count: {self.z_count}", font=("Arial", 12))
        self.z_label.pack()

        self.x_label = tk.Label(self, text=f"'x' count: {self.x_count}", font=("Arial", 12))
        self.x_label.pack()

        self.total_label = tk.Label(self, text=f'total count: {self.z_count + self.x_count}')
        self.total_label.pack()

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

    def start_timer(self, event):
        if not self.timer_running:
            self.timer_running = True
            self.label.config(text="Timer started! Press 'z' or 'x' to count")
            self.after(60000, self.stop_timer)  # 60000 ms = 1 minute

    def stop_timer(self):
        self.timer_running = False
        self.label.config(text="Timer ended")
        self.total_label.pack()


if __name__ == "__main__":
    app = KeyCounter()
    app.mainloop()
