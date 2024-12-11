import heapq
from enums import State

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

def get_neighbors(grid, row, col, consider_obstacles=True, return_format="coords"):
    """
    UNTESTED: Returns a list of adjacent positions/direction-strings via Von Neumann neighborhood.
    
    :param bool consider_obstacles: option to also consider pits/wumpi as neighboors
    :param string return_format: option to configure return ("coords"->coordinates, "full"->coordinates and directions)
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
            
            # optional: agents should go around pits and wumpi
            if consider_obstacles == True:
                if (grid[n_row][n_col] == State.PIT 
                or grid[n_row][n_col] == State.S_WUMPUS
                or grid[n_row][n_col] == State.L_WUMPUS):
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

def a_star_search(grid, start, goal):
    """
    UNTESTED: Performs an A*-Search on a given agent's knowledge-grid. Uses Manhattan-distance to calculate the shortest path to a target position.
    
    :param 2D-list grid: knowledge grid, will construct a path through fields with State.safe or None
    :param (int,int) start: starting position for the agent
    :param (int,int) goal: target position for the agent (e.g. another agent's position to go to)
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

        neighbors = get_neighbors(grid, current[0], current[1])
        
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