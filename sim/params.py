from dataclasses import dataclass

@dataclass
class Params:
    dt: float = 1.0 / 240.0 #240 Hz

    # Force targets (N)
    # F_des: float = 6.0
    # F_max: float = 10.0  # hard cap
    F_des: float = 80.0
    F_max: float = 90.0  # hard cap

    # Force regulation
    k_force: float = 0.0008   # (meters per Newton) mapped into jaw travel command
    close_speed: float = 0.0006  # meters/step while searching for contact

    # Contact detection and stability
    contact_threshold: float = 0.5
    stable_band: float = 1.0
    settle_steps: int = 120  # ~0.5s at 240Hz
    # settle_steps: int = 5 # for faster testing

    # Jaw command convention for this simplified gripper:
    # q_cmd = 0.0  -> fully open
    # q_cmd = q_max -> more closed (each jaw moves inward by q_cmd)
    q_open: float = 0.0
    q_closed: float = 0.02  # max inward travel for each jaw (meters)

    # Recovery
    emergency_open_step: float = 0.003

    # Lift (m, m/step)
    lift_speed: float = 0.0005
    lift_max: float = 0.12
    lift_force: float  = 200.0
    jaw_force: float = 80.0
