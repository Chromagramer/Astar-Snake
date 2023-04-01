import pygame
import random

# Set the screen size
SCREEN_WIDTH = 330
SCREEN_HEIGHT = 330
global_path = []
import heapq


# Define a heuristic function that estimates the distance from a node to the goal
def heuristic(current, end):
    return abs(end[0] - current[0]) + abs(end[1] - current[1])


# Define a function that returns a list of neighboring nodes that are not obstacles
def get_neighbors(current, obstacle_coordinate_list):
    x, y = current
    neighbors = [(x - 10, y), (x + 10, y), (x, y - 10), (x, y + 10)]
    return [n for n in neighbors if n not in obstacle_coordinate_list]


# Define the A* search function
def a_star(start, end, obstacle_coordinate_list):
    # Initialize the frontier with the starting node
    frontier = [(0, start)]
    # Initialize the came_from dictionary as an empty dictionary
    came_from = {}
    # Initialize the cost_so_far dictionary with the cost to reach the starting node
    cost_so_far = {start: 0}

    # While the frontier is not empty
    while frontier:
        # Pop the node with the lowest priority from the frontier
        _, current = heapq.heappop(frontier)

        # If the current node is the goal, reconstruct the path and return it
        if current == end:
            break

        # Check each neighbor of the current node
        for neighbor in get_neighbors(current, obstacle_coordinate_list):
            # Calculate the cost to reach the neighbor
            new_cost = cost_so_far[current] + 10

            if neighbor[0] < 0 or neighbor[0] > SCREEN_WIDTH - 10 or neighbor[1] < 0 or neighbor[
                1] > SCREEN_HEIGHT - 10:
                continue

            # If the neighbor is not in the cost_so_far dictionary or the new cost is lower than the old cost, update the neighbor
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, end)
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current

    # Reconstruct the path by following the came_from dictionary from the end node to the start node
    path = []
    current = end
    while current != start:
        path.append(current)
        if current not in came_from:
            return []
        current = came_from[current]
    path.append(start)
    path.reverse()

    return path


def avoid_obstacle(current_coordinate, obstacle_coordinate_list):
    x, y = current_coordinate
    for direction in ["LEFT", "RIGHT", "UP", "DOWN"]:
        new_coordinate = []
        if direction == "LEFT":
            new_coordinate = [x - 10, y]
        elif direction == "RIGHT":
            new_coordinate = [x + 10, y]
        elif direction == "UP":
            new_coordinate = [x, y - 10]
        elif direction == "DOWN":
            new_coordinate = [x, y + 10]
        if new_coordinate in obstacle_coordinate_list:
            continue
        if new_coordinate[0] < 0 or new_coordinate[0] > SCREEN_WIDTH - 10 or new_coordinate[1] < 0 or new_coordinate[
            1] > SCREEN_HEIGHT - 10:
            continue
        return direction
    return None


def judge(current_coordinate, end_coordinate, obstacle_coordinate_list):
    global global_path
    if len(global_path) == 0:
        global_path = a_star(tuple(current_coordinate), tuple(end_coordinate),
                             [tuple(c) for c in obstacle_coordinate_list])
        if len(global_path) > 0:
            global_path.pop(0)
    if global_path:
        next_coordinate = global_path.pop(0)
        if next_coordinate[0] < current_coordinate[0]:
            return "LEFT"
        elif next_coordinate[0] > current_coordinate[0]:
            return "RIGHT"
        elif next_coordinate[1] < current_coordinate[1]:
            return "UP"
        elif next_coordinate[1] > current_coordinate[1]:
            return "DOWN"
    else:
        return avoid_obstacle(current_coordinate, obstacle_coordinate_list)


def main():
    # Initialize Pygame
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Set the game title
    pygame.display.set_caption("Snake Game")

    # Set the game colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    # Set the game variables
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    food_pos = [random.randrange(1, SCREEN_WIDTH // 10) * 10, random.randrange(1, SCREEN_HEIGHT // 10) * 10]
    food_spawn = True
    direction = "RIGHT"
    change_to = direction
    score = 0

    # Set the game font
    font = pygame.font.SysFont('Arial', 25)
    # Set the game loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # elif event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_RIGHT:
            #         change_to = "RIGHT"
            #     elif event.key == pygame.K_LEFT:
            #         change_to = "LEFT"
            #     elif event.key == pygame.K_UP:
            #         change_to = "UP"
            #     elif event.key == pygame.K_DOWN:
            #         change_to = "DOWN"
        change_to = judge(snake_pos, food_pos, snake_body[1:])

        # Change direction if the key was pressed
        if change_to == "RIGHT" and direction != "LEFT":
            direction = "RIGHT"
        elif change_to == "LEFT" and direction != "RIGHT":
            direction = "LEFT"
        elif change_to == "UP" and direction != "DOWN":
            direction = "UP"
        elif change_to == "DOWN" and direction != "UP":
            direction = "DOWN"

        # Move the snake
        if direction == "RIGHT":
            snake_pos[0] += 10
        elif direction == "LEFT":
            snake_pos[0] -= 10
        elif direction == "UP":
            snake_pos[1] -= 10
        elif direction == "DOWN":
            snake_pos[1] += 10

        # Add new body segment
        snake_body.insert(0, list(snake_pos))
        if snake_pos == food_pos:
            food_spawn = False
            score += 1
        else:
            snake_body.pop()

        # Spawn new food
        if not food_spawn:
            food_pos = None
            while food_pos is None or food_pos in snake_body:
                food_pos = [random.randrange(1, SCREEN_WIDTH // 10) * 10, random.randrange(1, SCREEN_HEIGHT // 10) * 10]

        food_spawn = True

        # Draw background
        screen.fill(BLACK)

        # Draw the snake and the food
        for pos in snake_body:
            pygame.draw.rect(screen, WHITE, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # Check if the snake is out of bounds
        if snake_pos[0] < 0 or snake_pos[0] > SCREEN_WIDTH - 10 or snake_pos[1] < 0 or snake_pos[
            1] > SCREEN_HEIGHT - 10:
            pygame.quit()
            quit()

        # Check if the snake collided with itself
        for block in snake_body[1:]:
            if snake_pos == block:
                pygame.quit()
                quit()

        # Draw the score
        score_text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, (10, 10))

        # Update the screen
        pygame.display.update()

        # Set the game speed
        pygame.time.Clock().tick(60)


if __name__ == "__main__":
    main()
