import random

board = []
knowledge = []
visited = []

curr_pos = [0, 0]
facing = 'RIGHT'
wumpus_alive = True
alive = True
grid_size = 4
bump = False
scream = False

moves = {'w': (-1,0), 's': (1,0), 'a': (0,-1), 'd': (0,1)}
move_names = {'w': 'UP', 's': 'DOWN', 'a': 'LEFT', 'd': 'RIGHT'}

PERCEPT_NAMES = ['Stench', 'Breeze', 'Glitter', 'Bump', 'Scream']

def printGrid(grid, title):
    print(f"\n  {title}")
    n = len(grid)
    w = 12
    for r in range(n):
        print("  +" + (("-" * w + "+") * n))
        line = "  "
        for c in range(n):
            cell = grid[r][c]
            if isinstance(cell, list):
                if not cell:
                    content = "."
                else:
                    content = ",".join(cell)
            else:
                content = cell
            line += "|" + content.center(w)
        line += "|"
        print(line)
    print("  +" + (("-" * w + "+") * n))

def get_current_percepts():
    global bump, scream
    r, c = curr_pos
    cell_content = board[r][c]

    percepts = [None, None, None, None, None]

    if 'S' in cell_content:
        percepts[0] = 'Stench'
    if 'B' in cell_content:
        percepts[1] = 'Breeze'
    if 'G' in cell_content:
        percepts[2] = 'Glitter'
    if bump:
        percepts[3] = 'Bump'
        bump = False
    if scream:
        percepts[4] = 'Scream'
        scream = False

    return percepts

def get_adjacent_cells(r, c):
    adjacent = []
    deltas = [(-1,0), (1,0), (0,-1), (0,1)]
    for dr, dc in deltas:
        nr, nc = r + dr, c + dc
        if 0 <= nr < grid_size and 0 <= nc < grid_size:
            adjacent.append((nr, nc))
    return adjacent

def update_knowledge(percepts):
    global knowledge, visited
    r, c = curr_pos

    visited[r][c] = True

    k_content = []

    if percepts[0]:
        k_content.append('S')
    if percepts[1]:
        k_content.append('B')
    if percepts[2]:
        k_content.append('G')
    if percepts[4]:
        k_content.append('Scr')

    k_content.append('A')
    knowledge[r][c] = ",".join(k_content)

    update_danger_inference()

def update_danger_inference():
    global knowledge

    for r in range(grid_size):
        for c in range(grid_size):
            if visited[r][c]:
                continue

            possible_pit = False
            possible_wumpus = False
            confirmed_safe = True

            adjacent = get_adjacent_cells(r, c)
            has_visited_neighbor = False

            for nr, nc in adjacent:
                if visited[nr][nc]:
                    has_visited_neighbor = True
                    cell_k = knowledge[nr][nc]

                    if 'B' in cell_k:
                        possible_pit = True
                        confirmed_safe = False
                    if 'S' in cell_k:
                        possible_wumpus = True
                        confirmed_safe = False

            if not has_visited_neighbor:
                knowledge[r][c] = '?'
            else:
                dangers = []
                if possible_pit:
                    dangers.append('P?')
                if possible_wumpus:
                    dangers.append('W?')

                if dangers:
                    knowledge[r][c] = ",".join(dangers)
                elif confirmed_safe:
                    knowledge[r][c] = 'OK'
                else:
                    knowledge[r][c] = '?'

def clear_agent_marker(r, c):
    old_k = knowledge[r][c].split(",")
    if 'A' in old_k:
        old_k.remove('A')
    if not old_k:
        knowledge[r][c] = "OK"
    else:
        knowledge[r][c] = ",".join(old_k)

def add_adjacent_percept(r, c, item):
    deltas = [(-1,0), (1,0), (0,-1), (0,1)]
    for dr, dc in deltas:
        nr, nc = r + dr, c + dc
        if 0 <= nr < grid_size and 0 <= nc < grid_size:
            if item not in board[nr][nc]:
                board[nr][nc].append(item)

def parse_coordinate(prompt):
    while True:
        try:
            val = input(prompt).strip()
            if not val:
                return None
            parts = val.replace(',', ' ').split()
            if len(parts) != 2:
                print("  Please enter two numbers separated by space or comma.")
                continue
            r, c = map(int, parts)
            if 0 <= r < grid_size and 0 <= c < grid_size:
                return [r, c]
            else:
                print(f"  Coordinates must be between 0 and {grid_size-1}.")
        except ValueError:
            print("  Invalid input. Please enter numbers.")

def setup_game():
    global board, knowledge, visited, curr_pos, grid_size, wumpus_alive, alive, bump, scream

    print("=== Custom Wumpus Map Setup ===")

    while True:
        try:
            sz_str = input("Enter grid size N (default 4): ").strip()
            if not sz_str:
                grid_size = 4
            else:
                grid_size = int(sz_str)
                if grid_size < 2:
                    print("  Size must be at least 2.")
                    continue
            break
        except ValueError:
            print("  Invalid number.")

    while True:
        mode = input("Map Generation: (M)anual or (R)andom? ").strip().lower()
        if mode in ['m', 'r']:
            break
        print("  Please enter 'm' or 'r'.")

    board = [[[] for _ in range(grid_size)] for _ in range(grid_size)]
    knowledge = [['?'] * grid_size for _ in range(grid_size)]
    visited = [[False] * grid_size for _ in range(grid_size)]

    if mode == 'm':
        print(f"Grid is {grid_size}x{grid_size}. Coordinates are 0-indexed (0 to {grid_size-1}).")
        pos = parse_coordinate("Enter Agent start (row col): ")
        curr_pos = pos if pos else [grid_size-1, 0]

        g_pos = parse_coordinate("Enter Gold location (row col): ")
        if not g_pos:
            g_pos = [0, grid_size-1]
        board[g_pos[0]][g_pos[1]].append('G')

        w_pos = parse_coordinate("Enter Wumpus location (row col): ")
        if not w_pos:
            w_pos = [0, 0]
        board[w_pos[0]][w_pos[1]].append('W')
        add_adjacent_percept(w_pos[0], w_pos[1], 'S')

        num_pits = int(0.2 * grid_size * grid_size)
        print(f"\nTime to place {num_pits} pits (20% of {grid_size*grid_size} cells).")

        for i in range(num_pits):
            p_pos = parse_coordinate(f"Enter Pit #{i+1} loc (row col): ")
            if p_pos:
                if 'P' not in board[p_pos[0]][p_pos[1]]:
                    board[p_pos[0]][p_pos[1]].append('P')
                    add_adjacent_percept(p_pos[0], p_pos[1], 'B')
                else:
                    print("  Pit already there.")
    else:
        print("\n  >> Randomly generating map...")

        curr_pos = [random.randint(0, grid_size-1), random.randint(0, grid_size-1)]

        def get_random_pos(exclude_list):
            while True:
                r = random.randint(0, grid_size-1)
                c = random.randint(0, grid_size-1)
                if [r, c] not in exclude_list:
                    return [r, c]

        g_pos = get_random_pos([curr_pos])
        board[g_pos[0]][g_pos[1]].append('G')

        w_pos = get_random_pos([curr_pos])
        board[w_pos[0]][w_pos[1]].append('W')
        add_adjacent_percept(w_pos[0], w_pos[1], 'S')

        num_pits = int(0.2 * grid_size * grid_size)
        pits_placed = 0
        while pits_placed < num_pits:
            r = random.randint(0, grid_size-1)
            c = random.randint(0, grid_size-1)
            if [r, c] != curr_pos:
                if 'P' not in board[r][c]:
                    board[r][c].append('P')
                    add_adjacent_percept(r, c, 'B')
                    pits_placed += 1

    wumpus_alive = True
    alive = True
    bump = False
    scream = False

    print("\nMap Setup Complete!")

def format_percepts(percepts):
    result = "["
    for i, p in enumerate(percepts):
        if p is None:
            result += "None"
        else:
            result += f"'{p}'"
        if i < len(percepts) - 1:
            result += ", "
    result += "]"
    return result

def print_percept_legend():
    print("\n  Percept Format: [Stench, Breeze, Glitter, Bump, Scream]")

def print_inference_summary():
    print("\n  Danger Inference Summary:")
    print("  " + "-" * 40)

    dangers_found = False
    for r in range(grid_size):
        for c in range(grid_size):
            if not visited[r][c]:
                cell = knowledge[r][c]
                if 'P?' in cell or 'W?' in cell:
                    dangers_found = True
                    dangers = []
                    if 'P?' in cell:
                        dangers.append("Possible Pit (P?)")
                    if 'W?' in cell:
                        dangers.append("Possible Wumpus (W?)")
                    print(f"  Cell ({r},{c}): {', '.join(dangers)}")

    if not dangers_found:
        print("  No inferred dangers in unexplored cells.")
    print("  " + "-" * 40)

def play():
    global curr_pos, facing, bump, scream

    setup_game()

    print("=" * 50)
    print("       WUMPUS WORLD (Custom)")
    print("=" * 50)
    print("Controls: w=Up, s=Down, a=Left, d=Right")
    print("          q=Quit")
    print("Goal:     Reach the Gold.")
    print("=" * 50)
    print_percept_legend()

    update_knowledge(get_current_percepts())

    while True:
        current_percepts = get_current_percepts()

        printGrid(knowledge, "KNOWLEDGE GRID")
        print(f"\n  Position: {curr_pos}, Facing: {facing}")
        print(f"  Percepts: {format_percepts(current_percepts)}")

        print_inference_summary()

        r, c = curr_pos
        cell = board[r][c]

        if 'P' in cell:
            print("\n  You fell into a pit! GAME OVER")
            break

        if 'W' in cell and wumpus_alive:
            print("\n  You were eaten by the Wumpus! GAME OVER")
            break

        if 'G' in cell:
            print("\n  You found the GOLD! YOU WIN!")
            break

        cmd = input("\n  Action (w/a/s/d/q): ").strip().lower()

        if cmd == 'q':
            print("\n  Goodbye!")
            break

        if cmd in moves:
            new_facing = move_names[cmd]
            facing = new_facing

            dr, dc = moves[cmd]
            nr, nc = curr_pos[0] + dr, curr_pos[1] + dc

            if nr < 0 or nr >= grid_size or nc < 0 or nc >= grid_size:
                print("  >> Bump! You hit a wall.")
                bump = True
            else:
                clear_agent_marker(curr_pos[0], curr_pos[1])
                curr_pos = [nr, nc]
                print(f"  >> Moved {facing} to ({nr},{nc})")
                update_knowledge(get_current_percepts())
        else:
            print("  Invalid command.")

if __name__ == "__main__":
    play()
