import tkinter as tk
import random


CELL_SIZE = 20
GRID_W = 25
GRID_H = 20
DELAY = 120  

BG = "black"
SNAKE_COLOR = "lime"
FOOD_COLOR = "red"

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game by Taleb Amine")

        self.canvas = tk.Canvas(
            root,
            width=GRID_W * CELL_SIZE,
            height=GRID_H * CELL_SIZE,
            bg=BG,
            highlightthickness=0
        )
        self.canvas.pack()

        
        self.high_score = 0
        self.score = 0

        self.label = tk.Label(root, text="Score: 0   High Score: 0", font=("Arial", 14))
        self.label.pack()

        
        self.start_btn = tk.Button(root, text="START", font=("Arial", 14), command=self.start_game)
        self.restart_btn = tk.Button(root, text="RESTART", font=("Arial", 14), command=self.start_game)

    
        self.state = "menu"

        
        root.bind("<Up>", lambda e: self.change_dir(0, -1))
        root.bind("<Down>", lambda e: self.change_dir(0, 1))
        root.bind("<Left>", lambda e: self.change_dir(-1, 0))
        root.bind("<Right>", lambda e: self.change_dir(1, 0))
        root.bind("<space>", lambda e: self.start_game() if self.state != "running" else None)

        self.show_menu()
        self.game_loop()  

    def update_label(self):
        self.label.config(text=f"Score: {self.score}   High Score: {self.high_score}")

    def show_menu(self):
        self.canvas.delete("all")
        self.score = 0
        self.update_label()

        self.canvas.create_text(
            (GRID_W * CELL_SIZE) // 2,
            (GRID_H * CELL_SIZE) // 2 - 60,
            text="SNAKE",
            fill="white",
            font=("Arial", 28, "bold")
        )

        self.canvas.create_text(
            (GRID_W * CELL_SIZE) // 2,
            (GRID_H * CELL_SIZE) // 2 - 20,
            text="\nUse Arrow Keys to Move\nEat the red food to grow more\nPress Space to Start or Restart",
            fill="white",
            font=("Arial", 14),
            justify="center"
        )

        self.canvas.create_window(
            (GRID_W * CELL_SIZE) // 2,
            (GRID_H * CELL_SIZE) // 2 + 50,
            window=self.start_btn
        )

        self.state = "menu"

    def reset_game(self):
        self.score = 0
        self.update_label()

        cx, cy = GRID_W // 2, GRID_H // 2
        self.snake = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.dx, self.dy = 1, 0  

        self.spawn_food()

    def start_game(self):
        self.canvas.delete("all")
        self.reset_game()
        self.state = "running"

    def spawn_food(self):
        while True:
            x = random.randint(0, GRID_W - 1)
            y = random.randint(0, GRID_H - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                return

    def change_dir(self, dx, dy):
        if self.state != "running":
            return

        
        if (dx, dy) == (-self.dx, -self.dy):
            return
        self.dx, self.dy = dx, dy

    def draw_cell(self, x, y, color):
        x1 = x * CELL_SIZE
        y1 = y * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    def update(self):
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.dx, head_y + self.dy)

        
        if not (0 <= new_head[0] < GRID_W and 0 <= new_head[1] < GRID_H):
            self.state = "gameover"
            return

       
        if new_head in self.snake:
            self.state = "gameover"
            return

        self.snake.insert(0, new_head)

       
        if new_head == self.food:
            self.score += 1

           
            if self.score > self.high_score:
                self.high_score = self.score

            self.update_label()
            self.spawn_food()
        else:
            self.snake.pop()

    def render(self):
        self.canvas.delete("all")

       
        fx, fy = self.food
        self.draw_cell(fx, fy, FOOD_COLOR)

       
        for x, y in self.snake:
            self.draw_cell(x, y, SNAKE_COLOR)

    def show_game_over(self):
        
        if self.score > self.high_score:
            self.high_score = self.score
        self.update_label()

        self.canvas.delete("all")
        self.canvas.create_text(
            (GRID_W * CELL_SIZE) // 2,
            (GRID_H * CELL_SIZE) // 2 - 40,
            text="GAME OVER",
            fill="white",
            font=("Arial", 26, "bold")
        )
        self.canvas.create_text(
            (GRID_W * CELL_SIZE) // 2,
            (GRID_H * CELL_SIZE) // 2,
            text="Press RESTART or SPACE",
            fill="white",
            font=("Arial", 14)
        )

        self.canvas.create_window(
            (GRID_W * CELL_SIZE) // 2,
            (GRID_H * CELL_SIZE) // 2 + 50,
            window=self.restart_btn
        )

    def game_loop(self):
        if self.state == "running":
            self.update()
            if self.state == "running":
                self.render()
            else:
                self.show_game_over()

        self.root.after(DELAY, self.game_loop)


if __name__ == "__main__":
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()