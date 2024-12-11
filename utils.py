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

def get_neighbors(self, grid, row, col):
    """Returns a list of adjacent positions via Von Neumann neighborhood"""
    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]
        
    neighbors = []
    size = len(grid)

    for d_row, d_col in directions:
        n_row, n_col = row + d_row, col + d_col
        # Check if the new position is within bounds
        if 0 <= n_row < size and 0 <= n_col < size:
            neighbors.append((n_row, n_col))

    return neighbors