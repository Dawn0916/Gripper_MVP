import pybullet as p

# Define a Joint + contact / force proxy measurement 
def sum_fingertip_normal_forces(gripper_id: int, object_id: int, fingertip_links: set[int]) -> float:
    cps = p.getContactPoints(bodyA=gripper_id, bodyB=object_id) # Get contact points between gripper and object
    if not cps:
        return 0.0

    F = 0.0
    for cp in cps: # Loop over each contact point
        linkA = cp[3]          # link index on bodyA (gripper)
        normal_force = cp[9]   # normal force magnitude
        if linkA in fingertip_links:
            F += normal_force
    return F
