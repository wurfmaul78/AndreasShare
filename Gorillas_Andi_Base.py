import tkinter as tk
import math
import random 

WIDTH = 800
HEIGHT = 600
GRAVITY = 0.5
WINNING_SCORE = 10

class GorillaGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Gorillas – Python Edition")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="skyblue")
        self.canvas.pack()

        self.score = [0, 0]
        self.turn = 0
        self.wind = random.uniform(-1, 1)
        self.running = True

        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack()

        tk.Label(self.input_frame, text="Winkel (°):").pack(side=tk.LEFT)
        self.angle_entry = tk.Entry(self.input_frame, width=5)
        self.angle_entry.pack(side=tk.LEFT)

        tk.Label(self.input_frame, text="Geschwindigkeit:").pack(side=tk.LEFT)
        self.velocity_entry = tk.Entry(self.input_frame, width=5)
        self.velocity_entry.pack(side=tk.LEFT)

        self.throw_button = tk.Button(self.input_frame, text="Banane werfen", command=self.throw_banana)
        self.throw_button.pack(side=tk.LEFT)

        self.info_label = tk.Label(self.root, text="")
        self.info_label.pack()

        self.reset_game()

    def reset_game(self):
        self.canvas.delete("all")
        
        # Hintergrundschrift
        self.canvas.create_text(
            WIDTH // 2, 100,
            text="Speziell für Andreas",
            font=("Arial", 49, "bold"),
            fill="white",
            tags="skytext"
        )

        self.buildings = self.generate_buildings()
        self.draw_buildings()
        self.gorilla1 = self.place_gorilla(self.buildings[2])
        self.gorilla2 = self.place_gorilla(self.buildings[-3])
        self.draw_gorillas()
        self.update_info_label()

    def generate_buildings(self):
        buildings = []
        x = 0
        while x < WIDTH:
            w = random.randint(40, 70)
            h = random.randint(150, 400)
            rect = (x, HEIGHT - h, w, h)
            buildings.append(rect)
            x += w
        return buildings

    def draw_buildings(self):
        for x, y, w, h in self.buildings:
            self.canvas.create_rectangle(x, y, x + w, y + h, fill="slateblue")

    def place_gorilla(self, building):
        x, y, w, h = building
        gx = x + w // 2 - 10
        gy = y - 20
        return (gx, gy)

    def draw_gorillas(self):
        self.canvas.create_oval(*self.gorilla1, self.gorilla1[0]+20, self.gorilla1[1]+20, fill="magenta", tag="gorilla")
        self.canvas.create_oval(*self.gorilla2, self.gorilla2[0]+20, self.gorilla2[1]+20, fill="magenta", tag="gorilla")

    def throw_banana(self):
        if not self.running:
            return

        try:
            angle = float(self.angle_entry.get())
            velocity = float(self.velocity_entry.get())
        except ValueError:
            self.info_label.config(text="Bitte gültige Zahlen eingeben.")
            return

        self.canvas.delete("banana")
        start_x, start_y = self.gorilla1 if self.turn == 0 else self.gorilla2
        self.banana_x = start_x + 10
        self.banana_y = start_y + 10

        rad = math.radians(angle)
        dir = 1 if self.turn == 0 else -1
        self.banana_vx = dir * velocity * math.cos(rad) + self.wind
        self.banana_vy = -velocity * math.sin(rad)

        self.animate_banana()

    def animate_banana(self):
        self.banana_vy += GRAVITY
        self.banana_x += self.banana_vx
        self.banana_y += self.banana_vy

        self.canvas.delete("banana")
        self.canvas.create_oval(self.banana_x - 5, self.banana_y - 5,
                                self.banana_x + 5, self.banana_y + 5,
                                fill="yellow", tag="banana")

        if self.hit_gorilla():
            self.score[self.turn] += 1
            if self.score[self.turn] >= WINNING_SCORE:
                self.info_label.config(text=f"Spieler {self.turn + 1} hat das Spiel gewonnen!")
                self.canvas.create_text(
                    WIDTH//2, 200,
                    text=f"🎉 Spieler {self.turn + 1} gewinnt! 🎉",
                    font=("Arial", 36, "bold"),
                    fill="red"
                )
                self.running = False
                return
            else:
                self.info_label.config(text=f"Treffer! Spieler {self.turn + 1} hat jetzt {self.score[self.turn]} Punkte.")
                self.turn = 1 - self.turn
                self.wind = random.uniform(-1, 1)
                self.root.after(2000, self.reset_game)
                return

        if self.banana_y > HEIGHT or self.banana_x < 0 or self.banana_x > WIDTH:
            self.turn = 1 - self.turn
            self.wind = random.uniform(-1, 1)
            self.update_info_label()
            return

        self.root.after(30, self.animate_banana)

    def hit_gorilla(self):
        gx, gy = self.gorilla2 if self.turn == 0 else self.gorilla1
        return gx < self.banana_x < gx + 20 and gy < self.banana_y < gy + 20

    def update_info_label(self):
        self.info_label.config(
            text=f"Spieler {self.turn + 1} ist dran – Punkte: P1={self.score[0]} | P2={self.score[1]} – Wind: {self.wind:.2f}"
        )

if __name__ == "__main__":
    root = tk.Tk()
    game = GorillaGame(root)
    root.mainloop()