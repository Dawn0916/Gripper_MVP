import pybullet as p

def create_parallel_gripper_with_lift(
    base_pos=(0.50, 0.0, 0.03),
    base_euler=(0.0, 0.0, 0.0),
    gap_open=0.10,
) -> int:
    """
    Multibody structure (joint indices):
      joint 0: lift prismatic (Z)
      joint 1: left jaw prismatic (Y inward)
      joint 2: right jaw prismatic (Y inward)

    Link indices used by contacts:
      link 0: lift carriage
      link 1: left jaw
      link 2: right jaw
    """

    base_orn = p.getQuaternionFromEuler(base_euler)

    # Visual/Collision sizes (half extents)
    anchor_size  = (0.02, 0.02, 0.01)
    carriage_size= (0.03, 0.03, 0.01)
    jaw_size     = (0.05, 0.006, 0.012)

    anchor_col   = p.createCollisionShape(p.GEOM_BOX, halfExtents=anchor_size)
    carriage_col = p.createCollisionShape(p.GEOM_BOX, halfExtents=carriage_size)
    jaw_col      = p.createCollisionShape(p.GEOM_BOX, halfExtents=jaw_size)

    anchor_vis   = p.createVisualShape(p.GEOM_BOX, halfExtents=anchor_size, rgbaColor=[0.01, 0.01, 0.01, 1])
    carriage_vis = p.createVisualShape(p.GEOM_BOX, halfExtents=carriage_size, rgbaColor=[0.45, 0.45, 0.45, 1])
    jaw_vis      = p.createVisualShape(p.GEOM_BOX, halfExtents=jaw_size, rgbaColor=[0.5, 0.5, 0.5, 1])

    half_gap = gap_open / 2.0

    # We will create 3 links: carriage, left jaw, right jaw
    link_masses = [1.0, 0.2, 0.2]
    link_cols   = [carriage_col, jaw_col, jaw_col]
    link_viss   = [carriage_vis, jaw_vis, jaw_vis]

    # Link frames relative to their parent:
    # carriage attached to anchor; jaws attached to carriage
    link_positions = [
        [0.0, 0.0, 0.0],          # carriage relative to anchor
        [0.03, +half_gap, 0.0],   # left jaw relative to carriage
        [0.03, -half_gap, 0.0],   # right jaw relative to carriage
    ]
    link_orientations = [[0,0,0,1]] * 3
    inertial_pos = [[0,0,0]] * 3
    inertial_orn = [[0,0,0,1]] * 3

    link_parent_indices = [0, 1, 1]  # carriage parent=anchor(base), jaws parent=carriage(link0)
    link_joint_types = [p.JOINT_PRISMATIC, p.JOINT_PRISMATIC, p.JOINT_PRISMATIC]
    link_joint_axes = [
        [0, 0, 1],   # lift in Z
        [0, -1, 0],  # left jaw inward when q increases
        [0, +1, 0],  # right jaw inward when q increases
    ]

    gid = p.createMultiBody(
        baseMass=0.0,  # anchor is fixed
        baseCollisionShapeIndex=anchor_col,
        baseVisualShapeIndex=anchor_vis,
        basePosition=list(base_pos),
        baseOrientation=base_orn,

        linkMasses=link_masses,
        linkCollisionShapeIndices=link_cols,
        linkVisualShapeIndices=link_viss,
        linkPositions=link_positions,
        linkOrientations=link_orientations,
        linkInertialFramePositions=inertial_pos,
        linkInertialFrameOrientations=inertial_orn,
        linkParentIndices=link_parent_indices,
        linkJointTypes=link_joint_types,
        linkJointAxis=link_joint_axes,
    )

    # Initialize joint states
    p.resetJointState(gid, 0, 0.0)  # lift z=0
    p.resetJointState(gid, 1, 0.0)  # left jaw open
    p.resetJointState(gid, 2, 0.0)  # right jaw open

    # Friction helps stable grasp
    for link in [-1, 0, 1, 2]:
        p.changeDynamics(gid, link, lateralFriction=1.0)

    return gid


def set_jaw_position(gripper_id: int, q_cmd: float, max_force: float = 80.0) -> None:
    """Control jaw joints (joints 1 and 2). q_cmd in meters (0=open, larger=close)."""
    for jid in (1, 2):
        p.setJointMotorControl2(
            gripper_id, jid,
            controlMode=p.POSITION_CONTROL,
            targetPosition=float(q_cmd),
            force=float(max_force),
        )

def set_lift_position(gripper_id: int, z_cmd: float, max_force: float = 200.0) -> None:
    """Control lift joint (joint 0). z_cmd in meters."""
    p.setJointMotorControl2(
        gripper_id, 0,
        controlMode=p.POSITION_CONTROL,
        targetPosition=float(z_cmd),
        force=float(max_force),
    )

