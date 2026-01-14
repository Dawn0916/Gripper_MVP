import os
import time
import pybullet as p

from sim.params import Params
from sim.scene import setup_world, set_camera, spawn_box_object
from sim.gripper import create_parallel_gripper_with_lift, set_lift_position, set_jaw_position
from sim.sensing import sum_fingertip_normal_forces
from sim.fsm import FSM


def main():
    prm = Params()

    # setup_world(dt=prm.dt, gui=True)
    # set_camera(target=(0.54, 0.0, 0.04), distance=0.45, yaw=45, pitch=-25) # Move camera closer to see the gripper and object

    use_gui = os.environ.get("PYBULLET_GUI", "0") == "1"
    print(f"Using GUI: {use_gui}")
    setup_world(dt=prm.dt, gui=use_gui)

    if use_gui:
        set_camera(target=(0.54, 0.0, 0.04), distance=0.45, yaw=45, pitch=-25) # Move camera closer to see the gripper and object
    
    

    # Create gripper with lift joint
    gripper = create_parallel_gripper_with_lift(
        base_pos=(0.50, 0.0, 0.03),
        gap_open=0.06
    )

    # Spawn box ON the ground
    half_extents = (0.015, 0.02, 0.03)
    obj = spawn_box_object(
        pos=(0.56, 0.0, half_extents[2]),  # z = 0.03 -> resting on plane
        half_extents=half_extents,
        mass=0.05
    )

    # Jaw links for force sensing
    fingertip_links = {0, 1}

    fsm = FSM(q_open=prm.q_open, q_closed=prm.q_closed)
   
    # Start open at ground level
    set_jaw_position(gripper, fsm.q_cmd, max_force=prm.jaw_force)
    set_lift_position(gripper, 0.0, max_force=prm.lift_force)


    while True:
        p.stepSimulation()
        # update_params_from_gui(fsm, sliders)
        F_meas = sum_fingertip_normal_forces(gripper, obj, fingertip_links)
        state, q_cmd, z_cmd = fsm.step(F_meas, prm)
        print(f"State: {state.name}, F_meas: {F_meas:.3f} N, q_cmd: {q_cmd:.4f} m, z_cmd: {z_cmd:.4f} m") # For debugging

        # Apply commands
        set_jaw_position(gripper, q_cmd, max_force=prm.jaw_force)
        set_lift_position(gripper, z_cmd, max_force=prm.lift_force)

        # Sleep to roughly match real-time
        # time.sleep(prm.dt) 
        time.sleep(0.1)  # ensure at least some sleep to avoid busy loop


if __name__ == "__main__":
    main()

