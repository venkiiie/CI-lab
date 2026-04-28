import random

# ==============================
# SETUP ENVIRONMENT
# ==============================

def create_world():
    n = int(input("Enter number of rooms (>=4): "))
    if n < 4:
        print("Grid must be at least 4x4. Setting to 4.")
        n = 4

    world = {}
    sensors = {}
    cell_number = 1

    # Map cells with integers
    for i in range(1, n+1):
        for j in range(1, n+1):
            world[(i,j)] = {
                "number": cell_number,
                "wampus": False,
                "pit": False,
                "gold": False
            }
            sensors[(i,j)] = {
                "stench": False,
                "breeze": False,
                "glitter": False
            }
            cell_number += 1

    start = (1,1)

    # Place Wampus randomly (not at start)
    while True:
        wampus = (random.randint(1,n), random.randint(1,n))
        if wampus != start:
            world[wampus]["wampus"] = True
            break

    # Place Gold randomly (not at start, not in wampus/pit)
    while True:
        gold = (random.randint(1,n), random.randint(1,n))
        if gold != start and not world[gold]["wampus"]:
            world[gold]["gold"] = True
            sensors[gold]["glitter"] = True
            break

    # 20% pits
    total_cells = n*n
    pit_count = int(0.2 * total_cells)

    placed = 0
    while placed < pit_count:
        pit = (random.randint(1,n), random.randint(1,n))
        if pit != start and not world[pit]["wampus"] and not world[pit]["gold"] and not world[pit]["pit"]:
            world[pit]["pit"] = True
            placed += 1

    # Configure Sensors (Stench & Breeze)
    for (i,j) in world:
        if world[(i,j)]["wampus"]:
            for adj in get_adjacent(i,j,n):
                sensors[adj]["stench"] = True

        if world[(i,j)]["pit"]:
            for adj in get_adjacent(i,j,n):
                sensors[adj]["breeze"] = True

    return n, world, sensors, start


def get_adjacent(i,j,n):
    adj = []
    if i > 1: adj.append((i-1,j))
    if i < n: adj.append((i+1,j))
    if j > 1: adj.append((i,j-1))
    if j < n: adj.append((i,j+1))
    return adj


# ==============================
# MOVEMENT FUNCTIONS
# ==============================

def turn_left(direction):
    dirs = ["UP","LEFT","DOWN","RIGHT"]
    return dirs[(dirs.index(direction)+1)%4]

def turn_right(direction):
    dirs = ["UP","RIGHT","DOWN","LEFT"]
    return dirs[(dirs.index(direction)+1)%4]

def move_forward(position, direction, n):
    x,y = position

    if direction == "UP":
        x -= 1
    elif direction == "DOWN":
        x += 1
    elif direction == "LEFT":
        y -= 1
    elif direction == "RIGHT":
        y += 1

    if x < 1 or x > n or y < 1 or y > n:
        print("BUMP! You hit a wall.")
        return position, True  # bump

    return (x,y), False


# ==============================
# SHOOT FUNCTION
# ==============================

def shoot_arrow(position, direction, world, n):
    x,y = position

    while True:
        if direction == "UP":
            x -= 1
        elif direction == "DOWN":
            x += 1
        elif direction == "LEFT":
            y -= 1
        elif direction == "RIGHT":
            y += 1

        if x < 1 or x > n or y < 1 or y > n:
            break

        if world[(x,y)]["wampus"]:
            world[(x,y)]["wampus"] = False
            print("SCREAM! Wampus died.")
            return True

    print("Arrow missed.")
    return False


# ==============================
# DISPLAY FUNCTION
# ==============================

def display_world(world, n):
    print("\nWorld Map (Hidden hazards):")
    for i in range(1,n+1):
        for j in range(1,n+1):
            cell = world[(i,j)]
            if cell["wampus"]:
                print("W", end=" ")
            elif cell["pit"]:
                print("P", end=" ")
            elif cell["gold"]:
                print("G", end=" ")
            else:
                print(".", end=" ")
        print()
    print()


# ==============================
# GAME LOOP
# ==============================

def play_game():
    n, world, sensors, position = create_world()
    direction = "RIGHT"
    score = 0
    game_over = False

    display_world(world, n)

    while not game_over:
        print("\nCurrent Position:", position)
        print("Facing:", direction)
        print("Score:", score)

        # Show Sensors
        if sensors[position]["stench"]:
            print("Stench detected!")
        if sensors[position]["breeze"]:
            print("Breeze detected!")
        if sensors[position]["glitter"]:
            print("Glitter detected!")

        action = input("Action (forward, left, right, grab, shoot, exit): ").lower()

        if action == "forward":
            position, bump = move_forward(position, direction, n)

        elif action == "left":
            direction = turn_left(direction)

        elif action == "right":
            direction = turn_right(direction)

        elif action == "grab":
            if sensors[position]["glitter"]:
                print("Gold grabbed! You win!")
                world[position]["gold"] = False
                sensors[position]["glitter"] = False
                score += 1000
                game_over = True
            else:
                print("No gold here.")

        elif action == "shoot":
            score -= 10
            killed = shoot_arrow(position, direction, world, n)
            if killed:
                score += 500

        elif action == "exit":
            break

        # Check Death Conditions
        if world[position]["wampus"]:
            print("You were eaten by Wampus!")
            score -= 1000
            game_over = True

        if world[position]["pit"]:
            print("You fell into a Pit!")
            score -= 1000
            game_over = True

    print("\nGAME OVER")
    print("Final Score:", score)


# ==============================
# RUN GAME
# ==============================

play_game() 
