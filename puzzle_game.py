import tkinter as tk
from tkinter import messagebox, ttk
import random

class SlidingPuzzle:
    def __init__(self, root):
        self.root = root
        # Remove window-specific methods
        self.root.configure(bg="#2c3e50")
        
        # Game variables
        self.size = 3  # 3x3 puzzle
        self.tiles = []
        self.empty_pos = (2, 2)  # Bottom right corner
        self.moves = 0
        self.game_won = False
        
        # Create UI
        self.setup_ui()
        self.create_puzzle()
        
    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.root,
            text="SLIDING PUZZLE",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=10)
        
        # Moves counter
        self.moves_label = tk.Label(
            self.root,
            text="Moves: 0",
            font=("Arial", 14),
            bg="#2c3e50",
            fg="white"
        )
        self.moves_label.pack(pady=5)
        
        # Game frame
        self.game_frame = tk.Frame(self.root, bg="#34495e", relief=tk.RAISED, bd=3)
        self.game_frame.pack(pady=20)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg="#2c3e50")
        buttons_frame.pack(pady=10)
        
        # New game button
        new_game_btn = tk.Button(
            buttons_frame,
            text="New Game",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            command=self.new_game
        )
        new_game_btn.pack(side=tk.LEFT, padx=5)
        
        # Solve button
        solve_btn = tk.Button(
            buttons_frame,
            text="Solve",
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            command=self.solve_puzzle
        )
        solve_btn.pack(side=tk.LEFT, padx=5)
        
        # Instructions
        instruction_label = tk.Label(
            self.root,
            text="Click tiles to move them. Arrange numbers 1-8 in order with empty space at bottom right.",
            font=("Arial", 10),
            bg="#2c3e50",
            fg="white",
            wraplength=350
        )
        instruction_label.pack(pady=10)
        
    def create_puzzle(self):
        # Create tiles
        self.tiles = []
        numbers = list(range(1, 9)) + [None]  # 1-8 + empty space
        
        for i in range(self.size):
            row = []
            for j in range(self.size):
                if i == self.size - 1 and j == self.size - 1:
                    # Empty space
                    btn = tk.Button(
                        self.game_frame,
                        text="",
                        font=("Arial", 16, "bold"),
                        width=4,
                        height=2,
                        bg="#95a5a6",
                        relief=tk.RAISED,
                        bd=3
                    )
                    btn.grid(row=i, column=j, padx=2, pady=2)
                    row.append(None)
                else:
                    number = numbers.pop(0)
                    btn = tk.Button(
                        self.game_frame,
                        text=str(number),
                        font=("Arial", 16, "bold"),
                        width=4,
                        height=2,
                        bg="#3498db",
                        fg="white",
                        relief=tk.RAISED,
                        bd=3,
                        command=lambda x=i, y=j: self.move_tile(x, y)
                    )
                    btn.grid(row=i, column=j, padx=2, pady=2)
                    row.append(btn)
            self.tiles.append(row)
        
        self.shuffle_puzzle()
    
    def shuffle_puzzle(self):
        # Shuffle the puzzle by making random moves
        for _ in range(100):
            possible_moves = self.get_possible_moves()
            if possible_moves:
                move = random.choice(possible_moves)
                self.make_move(move[0], move[1])
        
        self.moves = 0
        self.game_won = False
        self.update_moves()
    
    def get_possible_moves(self):
        moves = []
        empty_row, empty_col = self.empty_pos
        
        # Check all adjacent positions
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row = empty_row + dr
            new_col = empty_col + dc
            
            if 0 <= new_row < self.size and 0 <= new_col < self.size:
                moves.append((new_row, new_col))
        
        return moves
    
    def move_tile(self, row, col):
        if self.game_won:
            return
            
        # Check if this tile can be moved
        empty_row, empty_col = self.empty_pos
        
        # Check if adjacent to empty space
        if (abs(row - empty_row) == 1 and col == empty_col) or \
           (abs(col - empty_col) == 1 and row == empty_row):
            self.make_move(row, col)
    
    def make_move(self, row, col):
        empty_row, empty_col = self.empty_pos
        
        # Swap tile with empty space
        self.tiles[empty_row][empty_col] = self.tiles[row][col]
        self.tiles[row][col] = None
        
        # Update empty position
        self.empty_pos = (row, col)
        
        # Update button positions
        if self.tiles[empty_row][empty_col]:
            self.tiles[empty_row][empty_col].grid(row=empty_row, column=empty_col)
            self.tiles[empty_row][empty_col].configure(
                command=lambda: self.move_tile(empty_row, empty_col)
            )
        
        # Create new empty button
        empty_btn = tk.Button(
            self.game_frame,
            text="",
            font=("Arial", 16, "bold"),
            width=4,
            height=2,
            bg="#95a5a6",
            relief=tk.RAISED,
            bd=3
        )
        empty_btn.grid(row=row, column=col, padx=2, pady=2)
        self.tiles[row][col] = empty_btn
        
        self.moves += 1
        self.update_moves()
        
        # Check if puzzle is solved
        if self.check_win():
            self.game_won = True
            messagebox.showinfo("Congratulations!", f"Puzzle solved in {self.moves} moves!")
    
    def check_win(self):
        # Check if numbers are in correct order
        expected = 1
        for i in range(self.size):
            for j in range(self.size):
                if i == self.size - 1 and j == self.size - 1:
                    # Should be empty
                    if self.tiles[i][j] is not None:
                        return False
                else:
                    # Should have correct number
                    if self.tiles[i][j] is None or self.tiles[i][j].cget("text") != str(expected):
                        return False
                    expected += 1
        return True
    
    def update_moves(self):
        self.moves_label.config(text=f"Moves: {self.moves}")
    
    def new_game(self):
        # Clear existing tiles
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        self.create_puzzle()
    
    def solve_puzzle(self):
        # Reset to solved state
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        # Create solved puzzle
        self.tiles = []
        number = 1
        
        for i in range(self.size):
            row = []
            for j in range(self.size):
                if i == self.size - 1 and j == self.size - 1:
                    # Empty space
                    btn = tk.Button(
                        self.game_frame,
                        text="",
                        font=("Arial", 16, "bold"),
                        width=4,
                        height=2,
                        bg="#95a5a6",
                        relief=tk.RAISED,
                        bd=3
                    )
                    btn.grid(row=i, column=j, padx=2, pady=2)
                    row.append(None)
                else:
                    btn = tk.Button(
                        self.game_frame,
                        text=str(number),
                        font=("Arial", 16, "bold"),
                        width=4,
                        height=2,
                        bg="#3498db",
                        fg="white",
                        relief=tk.RAISED,
                        bd=3,
                        command=lambda x=i, y=j: self.move_tile(x, y)
                    )
                    btn.grid(row=i, column=j, padx=2, pady=2)
                    row.append(btn)
                    number += 1
            self.tiles.append(row)
        
        self.empty_pos = (self.size - 1, self.size - 1)
        self.moves = 0
        self.game_won = False
        self.update_moves()

class NumberPuzzle:
    def __init__(self, root):
        self.root = root
        # Remove window-specific methods
        self.root.configure(bg="#2c3e50")
        
        # Game variables
        self.numbers = []
        self.selected_number = None
        self.score = 0
        self.time_left = 120
        self.game_running = False
        
        self.setup_ui()
        self.generate_numbers()
        
    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.root,
            text="NUMBER PUZZLE",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=10)
        
        # Score and time frame
        info_frame = tk.Frame(self.root, bg="#2c3e50")
        info_frame.pack(pady=5)
        
        self.score_label = tk.Label(
            info_frame,
            text="Score: 0",
            font=("Arial", 14),
            bg="#2c3e50",
            fg="white"
        )
        self.score_label.pack(side=tk.LEFT, padx=20)
        
        self.time_label = tk.Label(
            info_frame,
            text="Time: 120s",
            font=("Arial", 14),
            bg="#2c3e50",
            fg="white"
        )
        self.time_label.pack(side=tk.RIGHT, padx=20)
        
        # Game area
        game_frame = tk.Frame(self.root, bg="#34495e", relief=tk.RAISED, bd=3)
        game_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Numbers grid
        self.numbers_frame = tk.Frame(game_frame, bg="#34495e")
        self.numbers_frame.pack(pady=20)
        
        # Instructions
        instruction_label = tk.Label(
            game_frame,
            text="Click numbers in ascending order (1, 2, 3, ...) to score points!",
            font=("Arial", 12),
            bg="#34495e",
            fg="white",
            wraplength=400
        )
        instruction_label.pack(pady=10)
        
        # Start button
        self.start_button = tk.Button(
            self.root,
            text="START GAME",
            font=("Arial", 14, "bold"),
            bg="#27ae60",
            fg="white",
            command=self.start_game,
            width=15
        )
        self.start_button.pack(pady=10)
        
    def generate_numbers(self):
        # Clear existing buttons
        for widget in self.numbers_frame.winfo_children():
            widget.destroy()
        
        # Generate random numbers 1-16
        self.numbers = list(range(1, 17))
        random.shuffle(self.numbers)
        
        # Create number buttons
        for i, number in enumerate(self.numbers):
            row = i // 4
            col = i % 4
            
            btn = tk.Button(
                self.numbers_frame,
                text=str(number),
                font=("Arial", 16, "bold"),
                width=4,
                height=2,
                bg="#3498db",
                fg="white",
                relief=tk.RAISED,
                bd=3,
                command=lambda n=number: self.click_number(n)
            )
            btn.grid(row=row, column=col, padx=2, pady=2)
    
    def click_number(self, number):
        if not self.game_running:
            return
        
        if self.selected_number is None:
            # First click
            if number == 1:
                self.selected_number = number
                self.score += 10
                self.update_score()
                self.highlight_number(number)
            else:
                messagebox.showinfo("Wrong!", "Start with number 1!")
        else:
            # Subsequent clicks
            if number == self.selected_number + 1:
                self.selected_number = number
                self.score += 10
                self.update_score()
                self.highlight_number(number)
                
                if number == 16:
                    messagebox.showinfo("Perfect!", "You completed the sequence!")
                    self.selected_number = None
                    self.generate_numbers()
            else:
                self.score = max(0, self.score - 5)
                self.update_score()
                messagebox.showinfo("Wrong!", f"Expected {self.selected_number + 1}, got {number}")
    
    def highlight_number(self, number):
        # Find and highlight the clicked number
        for widget in self.numbers_frame.winfo_children():
            if widget.cget("text") == str(number):
                widget.configure(bg="#e74c3c")
                break
    
    def update_score(self):
        self.score_label.config(text=f"Score: {self.score}")
    
    def start_game(self):
        if not self.game_running:
            self.game_running = True
            self.score = 0
            self.time_left = 120
            self.selected_number = None
            self.start_button.config(state=tk.DISABLED)
            self.generate_numbers()
            self.update_score()
            self.update_timer()
    
    def update_timer(self):
        if self.game_running and self.time_left > 0:
            self.time_left -= 1
            self.time_label.config(text=f"Time: {self.time_left}s")
            self.root.after(1000, self.update_timer)
        elif self.time_left <= 0:
            self.end_game()
    
    def end_game(self):
        self.game_running = False
        self.start_button.config(state=tk.NORMAL, text="PLAY AGAIN")
        messagebox.showinfo("Game Over!", f"Final Score: {self.score}")

def main():
    root = tk.Tk()
    
    # Create notebook for multiple puzzle games
    notebook = tk.ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Sliding Puzzle tab
    sliding_frame = tk.Frame(notebook)
    notebook.add(sliding_frame, text="Sliding Puzzle")
    sliding_puzzle = SlidingPuzzle(sliding_frame)
    
    # Number Puzzle tab
    number_frame = tk.Frame(notebook)
    notebook.add(number_frame, text="Number Puzzle")
    number_puzzle = NumberPuzzle(number_frame)
    
    root.mainloop()

if __name__ == "__main__":
    main() 