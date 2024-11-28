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