from binary_heap import BinaryHeap
import math
import time

class GridWorld:
    def __init__(self, filename):
        self.filename = filename
        self.grid = self.load_gridworld(filename)
        self.width = len(self.grid[0])
        self.height = len(self.grid)

    def load_gridworld(self, filename):
        with open(filename, 'r') as file:
            grid = [list(line.strip()) for line in file]
        return grid

    def is_blocked(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x] == '1'
        return True  # Consider out-of-bounds as blocked

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def heuristic(start, goal):
    return manhattan_distance(start[0], start[1], goal[0], goal[1])

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]

def a_star_search(grid_world, start, goal):
    open_list = BinaryHeap()
    open_list.insert((0, 0, start))  # Adding 0 as the tie-breaker initially
    came_from = {}
    g_values = {start: 0}

    num_expansions = 0

    while open_list.heap:
        current_f, _, current = open_list.pop()  # Include tie-breaker in the tuple
        num_expansions += 1
        if current == goal:
            return reconstruct_path(came_from, current), num_expansions

        x, y = current
        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        for neighbor in neighbors:
            if grid_world.is_blocked(*neighbor):
                continue
            tentative_g = g_values[current] + 1
            if neighbor not in g_values or tentative_g < g_values[neighbor]:
                g_values[neighbor] = tentative_g
                f_value = tentative_g + heuristic(neighbor, goal)
                # Include tie-breaker in the tuple
                open_list.insert((f_value, -tentative_g, neighbor))  # Using -g as the tie-breaker
                came_from[neighbor] = current

    return None, num_expansions  # No path found

def repeated_backward_a_star(grid_world):
    start = None
    goal = None

    # Initialize start and goal based on the grid
    for y, row in enumerate(grid_world.grid):
        for x, cell in enumerate(row):
            if cell == 'S':
                start = (x, y)
            elif cell == 'G':
                goal = (x, y)
            if start and goal:
                break
        if start and goal:
            break

    if not (start and goal):
        raise ValueError("Start or goal not found in the grid world.")

    total_path = []
    total_expansions = 0
    current_position = start
    start_time = time.time()

    while current_position != goal:
        path, num_expansions = a_star_search(grid_world, goal, current_position)  # Reverse the search direction
        total_expansions += num_expansions
        if not path:
            return None, total_expansions, time.time() - start_time
        # Reverse the path for backward A*
        path = path[::-1]
        next_position = path[1] if len(path) > 1 else goal

        if grid_world.is_blocked(*next_position):
            # Update the grid to mark the detected block and restart from the current position
            grid_world.grid[next_position[1]][next_position[0]] = '1'
        else:
            total_path.append(next_position)
            current_position = next_position

    return total_path, total_expansions, time.time() - start_time

def main_repeated_backward_a_star(filename):
    grid_world = GridWorld(filename)
    path, num_expansions, duration = repeated_backward_a_star(grid_world)
    if path:
        print("Path found:")
        for x, y in reversed(path):
            print(f"({x}, {y})")
        print(f"Path length: {len(path)}")
        print(f"Number of node expansions: {num_expansions}")
        print(f"Time taken: {duration} seconds")
    else:
        print("No path found.")
    return path
