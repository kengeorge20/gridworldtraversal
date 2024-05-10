from binary_heap import BinaryHeap
import math
import time

class GridWorld:
    def __init__(self, filename):
        self.filename = filename
        self.grid = self.load_gridworld(filename)
        self.width = len(self.grid[0])
        self.height = len(self.grid)
        self.h_values = {}  # For adaptive heuristic

    def load_gridworld(self, filename):
        with open(filename, 'r') as file:
            grid = [list(line.strip()) for line in file]
        return grid

    def is_blocked(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x] == '1'
        return True  # Consider out-of-bounds as blocked

    def update_h_values(self, expanded_nodes, goal, g_goal):
        # Only update nodes that were expanded
        for node in expanded_nodes:
            self.h_values[node] = g_goal - self.g_values.get(node, 0)

    def initialize_h_values(self, goal):
        for y in range(self.height):
            for x in range(self.width):
                self.h_values[(x, y)] = manhattan_distance(x, y, goal[0], goal[1])

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def heuristic(grid_world, node, goal):
    # Use updated heuristic values if available
    return grid_world.h_values.get(node, manhattan_distance(node[0], node[1], goal[0], goal[1]))

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]

def adaptive_a_star_search(grid_world, start, goal):
    open_list = BinaryHeap()
    came_from = {}
    grid_world.g_values = {start: 0}  # g_values needs to be accessible for heuristic update
    expanded_nodes = set()  # Track nodes expanded in the current search

    # Initialize open list with the start node
    h_start = heuristic(grid_world, start, goal)
    open_list.insert((h_start, 0, start))  # f-value, tie-breaker (g-value), node

    while open_list.heap:
        current_f, _, current = open_list.pop()
        if current == goal:
            # Update heuristic values for all expanded nodes before returning the path
            grid_world.update_h_values(expanded_nodes, goal, grid_world.g_values[goal])
            return reconstruct_path(came_from, current), len(expanded_nodes)

        expanded_nodes.add(current)  # Mark the current node as expanded

        x, y = current
        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        for neighbor in neighbors:
            if grid_world.is_blocked(*neighbor):
                continue
            tentative_g = grid_world.g_values[current] + 1
            if neighbor not in grid_world.g_values or tentative_g < grid_world.g_values[neighbor]:
                grid_world.g_values[neighbor] = tentative_g
                h_value = heuristic(grid_world, neighbor, goal)
                f_value = tentative_g + h_value
                open_list.insert((f_value, -tentative_g, neighbor))  # Using -g as tie-breaker
                came_from[neighbor] = current

    return None, 0  # No path found

def adaptive_repeated_a_star(grid_world, start, goal):
    total_path = []
    total_expansions = 0
    start_time = time.time()

    grid_world.initialize_h_values(goal)  # Initialize heuristic values based on Manhattan distance

    while True:
        path, num_expansions = adaptive_a_star_search(grid_world, start, goal)
        total_expansions += num_expansions
        if not path:
            return None, total_expansions, time.time() - start_time
        total_path.extend(path[:-1])  # Exclude the last node to not duplicate it in the next segment
        start = path[-1]  # Update start for the next iteration
        if start == goal:
            total_path.append(goal)  # Make sure the goal is included in the final path
            break
        # No need to update the grid for blocked cells in Adaptive A*

    return total_path, total_expansions, time.time() - start_time

def main_adaptive_a_star(filename):
    grid_world = GridWorld(filename)
    start, goal = (0, 0), (grid_world.width - 1, grid_world.height - 1)
    path, num_expansions, duration = adaptive_repeated_a_star(grid_world, start, goal)
    if path:
        print("Path found:")
        for x, y in path:
            print(f"({x}, {y})")
        print(f"Path length: {len(path)}")
    else:
        print("No path found")
    print(f"Total number of expansions: {num_expansions}")
    print(f"Total duration: {duration} seconds")
    return path

