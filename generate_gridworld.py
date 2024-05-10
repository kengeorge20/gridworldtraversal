import random
import os
from collections import deque

def create_gridworlds_directory():
    dir_path = './gridworlds'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

def generate_gridworld_dfs(width, height):
    grid = [['0' for _ in range(width)] for _ in range(height)]
    visited = [[False for _ in range(width)] for _ in range(height)]

    def get_unvisited_neighbors(x, y, width, height, visited):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and not visited[ny][nx]:
                neighbors.append((nx, ny))
        return neighbors

    def is_safe_to_block(x, y, width, height):
        return not ((x == 0 and y == 0) or (x == width-1 and y == height-1))

    stack = [(0, 0)]  # Start from the top-left corner for simplicity

    while stack:
        x, y = stack.pop()
        visited[y][x] = True

        if is_safe_to_block(x, y, width, height) and random.random() < 0.3:
            grid[y][x] = '1'  # Blocked
        else:
            grid[y][x] = '0'  # Unblocked or start/goal
            neighbors = get_unvisited_neighbors(x, y, width, height, visited)
            random.shuffle(neighbors)  # Randomize neighbors
            stack.extend(neighbors)

    grid[0][0] = 'S'  # Ensure start is unblocked
    grid[height-1][width-1] = 'G'  # Ensure goal is unblocked

    # Check if there's a path from start to goal
    if not validate_path(grid, width, height):
        print("Path validation failed, marking as unsolvable...")
        return grid, False  # Return the grid and mark as unsolvable
    else:
        return grid, True  # Return the grid and mark as solvable

def validate_path(grid, width, height):
    """Validate there's a path from S to G using BFS."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    start, goal = (0, 0), (height-1, width-1)
    queue = deque([start])
    visited = set([start])

    while queue:
        x, y = queue.popleft()
        if (x, y) == goal:
            return True  # Path found

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited and grid[ny][nx] != '1':
                queue.append((nx, ny))
                visited.add((nx, ny))

    return False  # No path found

def save_gridworld(grid, filename, solvable):
    with open(filename, 'w') as file:
        for row in grid:
            file.write(''.join(row) + '\n')
    if not solvable:
        base_path, file_name = os.path.split(filename)
        new_filename = os.path.join(base_path, file_name.replace('.txt', '_unsolvable.txt'))
        os.rename(filename, new_filename)

def generate_multiple_gridworlds(width, height, count=50):
    dir_path = create_gridworlds_directory()
    for i in range(count):
        grid, solvable = generate_gridworld_dfs(width, height)
        filename = f"{dir_path}/gridworld_{i+1}.txt"
        save_gridworld(grid, filename, solvable)
    print(f"{count} gridworlds saved to {dir_path}")

if __name__ == "__main__":
    generate_multiple_gridworlds(101, 101, 50)
