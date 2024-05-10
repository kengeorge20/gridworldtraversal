import tkinter as tk
from tkinter import ttk, messagebox
import os
from repeated_forward_a_star import main_repeated_forward_a_star
from repeated_backwards_a_star import main_repeated_backward_a_star
from adaptive_a_star import main_adaptive_a_star

class GridworldViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gridworld Viewer")
        self.geometry("800x600")  # Adjusted window size for larger grids
        
        self.gridworld_directory = './gridworlds'
        self.gridworld_files = self.load_gridworld_filenames()
        
        if not self.gridworld_files:
            messagebox.showerror("Error", "No gridworld files found. Please ensure the 'gridworlds' directory exists and contains '.txt' files.")
            self.destroy()
            return

        self.create_widgets()
    
    def load_gridworld_filenames(self):
        try:
            filenames = [f for f in os.listdir(self.gridworld_directory) if f.endswith('.txt')]
            return filenames
        except FileNotFoundError:
            return []

    def create_widgets(self):
        self.file_selector = ttk.Combobox(self, values=self.gridworld_files)
        self.file_selector.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.display_button = tk.Button(self, text="Display Gridworld", command=self.display_gridworld)
        self.display_button.grid(row=0, column=1, padx=10, pady=10)

        # Dropdown for algorithms
        self.algorithm_var = tk.StringVar(self)
        self.algorithm_var.set("Repeated Forward A*")  # Default algorithm
        self.algorithm_selector = ttk.Combobox(self, textvariable=self.algorithm_var, values=["Repeated Forward A*", "Repeated Backwards A*", "Adaptive A*"])
        self.algorithm_selector.grid(row=0, column=2, padx=10, pady=10)

        # Button to run the selected algorithm
        self.run_algorithm_button = tk.Button(self, text="Run Algorithm", command=self.run_selected_algorithm)
        self.run_algorithm_button.grid(row=0, column=3, padx=10, pady=10)
        
        self.canvas = tk.Canvas(self, bg="white", scrollregion=(0, 0, 1000, 1000))  # Expanded scroll region
        self.canvas.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Adding scrollbars
        hbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        hbar.grid(row=2, column=0, columnspan=4, sticky='we')
        hbar.config(command=self.canvas.xview)
        vbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vbar.grid(row=1, column=4, sticky='ns')
        vbar.config(command=self.canvas.yview)
        self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

    def display_gridworld(self):
        filename = self.file_selector.get()
        if filename:
            filepath = os.path.join(self.gridworld_directory, filename)
            with open(filepath, 'r') as file:
                lines = file.readlines()
            self.draw_gridworld(lines)

    def draw_gridworld(self, lines):
        self.canvas.delete("all")
        self.grid_height = len(lines)
        self.grid_width = max(len(line.strip()) for line in lines)
        self.max_dim = max(self.grid_height, self.grid_width)
        max_dim = max(len(lines), len(lines[0].strip()))  # Determine the larger dimension for cell size calculation
        cell_size = min(800 // max_dim, 600 // max_dim)  # Dynamically adjust cell size based on grid size
        
        for y, line in enumerate(lines):
            for x, char in enumerate(line.strip()):
                fill_color = "white"
                if char == '1':
                    fill_color = "black"
                elif char == 'S':
                    fill_color = "green"
                elif char == 'G':
                    fill_color = "red"
                self.canvas.create_rectangle(x*cell_size, y*cell_size, (x+1)*cell_size, (y+1)*cell_size, fill=fill_color)
        self.canvas.config(scrollregion=(0, 0, cell_size*max_dim, cell_size*max_dim))

    def run_selected_algorithm(self):
        selected_algorithm = self.algorithm_var.get()
        path = None  # Initialize path variable
        filename = self.file_selector.get()
        if filename:
            filepath = os.path.join(self.gridworld_directory, filename)
            if selected_algorithm == "Repeated Forward A*":
                path = main_repeated_forward_a_star(filepath)  # Assume this returns a list of (x, y) tuples
            elif selected_algorithm == "Repeated Backwards A*":
                path = main_repeated_backward_a_star(filepath)
            elif selected_algorithm == "Adaptive A*":
                path = main_adaptive_a_star(filepath)

            if path is not None:
                self.draw_path(path)

    def draw_path(self, path):
        cell_size = min(800 // self.max_dim, 600 // self.max_dim)  # Use the same cell size calculation logic
        for x, y in path:
            self.canvas.create_rectangle(x*cell_size, y*cell_size, (x+1)*cell_size, (y+1)*cell_size, fill="blue", outline="gray")

if __name__ == "__main__":
    app = GridworldViewer()
    app.mainloop()