import tkinter as tk
import random

class ClickDashGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Click-Dash Pro")
        self.root.geometry("600x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#0F172A") # Deep slate background

        # --- Game Constants & State ---
        self.score = 0
        self.time_left = 30
        self.is_running = False

        self.setup_ui()

    def setup_ui(self):
        """Builds a structured layout with a Header and a Game Area."""
        # --- Top Info Bar ---
        self.header = tk.Frame(self.root, bg="#1E293B", pady=15, padx=20)
        self.header.pack(fill="x")

        self.score_lbl = tk.Label(self.header, text=f"Score: {self.score}", 
                                  font=("Helvetica", 16, "bold"), bg="#1E293B", fg="#38BDF8")
        self.score_lbl.pack(side="left")

        self.timer_lbl = tk.Label(self.header, text=f"Time: {self.time_left}s", 
                                  font=("Helvetica", 16, "bold"), bg="#1E293B", fg="#FB7185")
        self.timer_lbl.pack(side="right")

        # --- Game Playground ---
        # We use a Canvas or a Frame as the 'Playground' to contain the button movement
        self.playground = tk.Frame(self.root, bg="#0F172A", bd=2, relief="flat")
        self.playground.pack(fill="both", expand=True, padx=20, pady=20)

        # The Target Button
        self.target_btn = tk.Button(self.playground, text="CLICK ME!", font=("Arial", 11, "bold"),
                                    bg="#4ADE80", fg="#064E3B", activebackground="#22C55E",
                                    relief="flat", cursor="target", command=self.handle_click)
        
        # Start Overlay (Covers the playground initially)
        self.overlay = tk.Frame(self.playground, bg="#1E293B")
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        tk.Label(self.overlay, text="READY?", font=("Helvetica", 24, "bold"), 
                 bg="#1E293B", fg="white").pack(pady=(150, 20))
        
        tk.Button(self.overlay, text="START GAME", font=("Helvetica", 12, "bold"), 
                  bg="#38BDF8", fg="white", relief="flat", padx=20, pady=10,
                  command=self.start_game, cursor="hand2").pack()

    def start_game(self):
        """Initializes game state and hides the overlay."""
        self.score = 0
        self.time_left = 30
        self.is_running = True
        self.overlay.place_forget() # Hide start screen
        self.update_ui_stats()
        self.move_target()
        self.tick()

    def handle_click(self):
        """Increments score and teleports the button."""
        if self.is_running:
            self.score += 1
            self.update_ui_stats()
            self.move_target()

    def move_target(self):
        """Randomly places the target within the playground boundaries."""
        # Get dimensions of the playground
        p_width = self.playground.winfo_width()
        p_height = self.playground.winfo_height()

        # If dimensions aren't ready yet (init), use defaults
        if p_width <= 1: p_width, p_height = 560, 500

        # Calculate random coordinates while keeping the button inside
        new_x = random.randint(10, p_width - 100)
        new_y = random.randint(10, p_height - 50)
        
        self.target_btn.place(x=new_x, y=new_y)

    def update_ui_stats(self):
        self.score_lbl.config(text=f"Score: {self.score}")
        self.timer_lbl.config(text=f"Time: {self.time_left}s")

    def tick(self):
        """The core game loop timer."""
        if self.is_running and self.time_left > 0:
            self.time_left -= 1
            self.update_ui_stats()
            self.root.after(1000, self.tick)
        elif self.time_left <= 0:
            self.end_game()

    def end_game(self):
        """Stops the game and prompts for name."""
        self.is_running = False
        self.target_btn.place_forget()
        self.open_submit_window()

    def open_submit_window(self):
        """Clean Toplevel for score submission."""
        win = tk.Toplevel(self.root)
        win.title("Game Over!")
        win.geometry("350x180")
        win.configure(bg="#F1F5F9")
        win.grab_set()

        tk.Label(win, text="Time's Up!", font=("Helvetica", 18, "bold"), 
                 bg="#F1F5F9", fg="#0F172A").pack(pady=15)
        tk.Label(win, text=f"Final Score: {self.score}", font=("Helvetica", 12), 
                 bg="#F1F5F9").pack()

        entry = tk.Entry(win, font=("Helvetica", 12), width=20)
        entry.pack(pady=10)
        entry.insert(0, "Your Name")

        def save():
            name = entry.get()
            print(f"SAVED: {name} | {self.score}")
            win.destroy()
            self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

        tk.Button(win, text="Submit Score", bg="#10B981", fg="white", relief="flat",
                  font=("Helvetica", 10, "bold"), padx=10, command=save).pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = ClickDashGame(root)
    root.mainloop()