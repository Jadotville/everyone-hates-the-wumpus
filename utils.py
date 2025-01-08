import heapq
from enums import State
from random import random, shuffle

# these are utility functions, that can be freely used by other modules

def manhattan(pos_a, pos_b):
    """Calculate manhattan distance between position a and b"""
    return abs(pos_a[0] - pos_b[0]) + abs(pos_a[1] - pos_b[1])

def near_objects(pos, objects, dist=0):
    """
    Check, if a position is in the viscinity to any listed object
    
    :param (int,int) pos: target position to be ckecked
    :param list objects: list of objects with a position attribute, e.g. agents.position
    :param int dist: optional, manhattan distance determining the viscinity
    """
    for object in range(objects):
        if manhattan(pos, object.position) <= dist:
            return True
    return False

def get_neighbors(grid, row, col, consider_obstacles=False, return_format="coords", chance=1):
    """
    Returns a list of adjacent positions/direction-strings via Von Neumann neighborhood.
    
    :param bool consider_obstacles: option to also consider pits/wumpi as neighboors
    :param string return_format: option to configure return ("coords"->coordinates, "full"->coordinates and directions)
    :param float chance: optional value between [0,1] to only have a chance of considering something an obstacle (only works with consider_obstacles=True)
    """
    directions = [
        (-1, 0, "up"),
        (1, 0, "down"),
        (0, -1, "left"),
        (0, 1, "right")
    ]
        
    neighbors = []
    size = len(grid)

    for d_row, d_col, dir in directions:
        n_row, n_col = row + d_row, col + d_col
        
        # Check if the new position is within bounds
        if 0 <= n_row < size and 0 <= n_col < size:
            
            # optional: agents should go around pits and wumpi, but risks allowed
            if consider_obstacles and random() <= chance:
                if (State.PIT in grid[n_row][n_col]["state"] 
                or State.S_WUMPUS in grid[n_row][n_col]["state"]
                or State.L_WUMPUS in grid[n_row][n_col]["state"]):
                    continue
            
            # add coordinates or direction as string
            if return_format == "coords":
                neighbors.append((n_row, n_col))
            elif return_format == "full":
                neighbors.append((n_row, n_col, dir))
            else:
                print("utils: INFO-specified return_format-" + return_format + " in get_neighbors() defaulted to returning directions only.")
                neighbors.append((dir))

    return neighbors

def a_star_search(grid, start, goal, chance=1):
    """
    Performs an A*-Search on a given agent's knowledge-grid. Uses Manhattan-distance to calculate the shortest path to a target position.
    
    :param 2D-list grid: knowledge grid, will construct a path through fields with State.safe or None
    :param (int,int) start: starting position for the agent
    :param (int,int) goal: target position for the agent (e.g. another agent's position to go to)
    :param float chance: optional value between [0,1] to only have a chance of considering something an obstacle
    """

    if not goal:
        return None

    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: manhattan(start, goal)}
    
    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            return reconstruct_path(came_from, current)

        neighbors = get_neighbors(grid, current[0], current[1], consider_obstacles=True, chance=chance)
        
        for neighbor in neighbors:
            tentative_g_score = g_score[current] + 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + manhattan(neighbor, goal)
                heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None

def reconstruct_path(came_from, current):
    
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    total_path.reverse()
    return total_path

def convert_to_direction(pos_a, pos_b):
    """
    Transforms the difference of position a and b to a direction-string. Make sure, the positions have a manhattan-distance of 1. Possible returns:
    - "up"/"down"/"left"/"right"
    """
    if manhattan(pos_a, pos_b) != 1:
        print("utils: ERROR-couldn't convert " + str(pos_b) + "-" + str(pos_a) + " into a direction.")
        return None
    
    convert = {
        (-1, 0): "up",
        (1, 0): "down",
        (0, -1): "left",
        (0, 1): "right"
    }
    x = pos_b[0] - pos_a[0]
    y = pos_b[1] - pos_a[1]
    
    return convert[(x,y)]

def append_unique(list, value, safe=False):
    """
    Appends the value to the list only if it is not already present.
    
    :param bool safe: only append, if the item is not "blocked" (list-format: [{"state": [...], "blocks": y}, ...] appends only if value != y)
    """
    if safe:
        if value not in list["state"] and value not in list["blocks"]:
            list["state"].append(value)
    else:
        if value not in list:
            list.append(value)

def list_difference(list_a, list_b):
    """Returns a list of items exclusively in list_a."""
    return [item for item in list_a if item not in list_b]

def derange(list):
    """
    Shuffles the elements of a list so that no item remains in its original position.
    
    :param list list: The input list to shuffle.
    """
    if len(list) < 2:
        raise ValueError("utils: ERROR-List must have at least 2 elements to shuffle.")
    
    while True:
        shuffled = list[:]
        shuffle(shuffled)
        if all(original != shuffled[idx] for idx, original in enumerate(list)):
            return shuffled