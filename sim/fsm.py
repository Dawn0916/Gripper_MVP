from enum import Enum, auto
import numpy as np

class State(Enum):    
    CLOSE_TO_CONTACT = auto()
    FORCE_REGULATE = auto()
    HOLD = auto()
    LIFT = auto()
    FAIL_RECOVER = auto()

class FSM:
    """
    FSM for force-limited pinch + lift (fingers-only version).

    Jaw command convention:
      q_cmd = 0 -> open
      q_cmd increases -> close

    Lift command convention:
      z_cmd = 0 -> start height
      z_cmd increases -> lift
    """
    def __init__(self, q_open: float, q_closed: float):
        self.state = State.CLOSE_TO_CONTACT
        self.q_open = q_open
        self.q_closed = q_closed
        self.q_cmd = q_open
        self.stable_counter = 0
        self.z_cmd = 0.0 # lift height command

    def step(self, F_meas: float, prm) -> State:
        """
        Returns:
          state, q_cmd, z_cmd
        """
        if self.state == State.CLOSE_TO_CONTACT:
            # Close slowly until contact
            self.q_cmd = min(self.q_closed, self.q_cmd + prm.close_speed) # close slowly by increading q_cmd, cap at q_closed
            if F_meas > prm.contact_threshold:
                self.state = State.FORCE_REGULATE
                self.stable_counter = 0

        elif self.state == State.FORCE_REGULATE:
            # Safety: hard cap
            if F_meas > prm.F_max:
                self.q_cmd = max(self.q_open, self.q_cmd - prm.emergency_open_step) # open a bit (reduce q_cmd) but don't go below q_open
                self.state = State.FAIL_RECOVER
                self.stable_counter = 0
            else:
                # Force regulation: close more if force low, open if force high
                err = prm.F_des - F_meas # compute force error
                dq = prm.k_force * err # convert force error to position change
                self.q_cmd = float(np.clip(self.q_cmd + dq, self.q_open, self.q_closed)) # update q_cmd, clip to valid range

                if abs(err) < prm.stable_band: # If force error is within stable band long enough, transition to HOLD
                    self.stable_counter += 1
                    if self.stable_counter > prm.settle_steps:
                        self.state = State.HOLD
                else:
                    self.stable_counter = 0

        elif self.state == State.HOLD:
            # Keep regulating (robust)
            if F_meas > prm.F_max: # Still enforce safety while holding
                self.state = State.FAIL_RECOVER
                self.stable_counter = 0
            else: # Keep regulating even in HOLD (prevents drift/slip)
                err = prm.F_des - F_meas
                dq = prm.k_force * err
                self.q_cmd = float(np.clip(self.q_cmd + dq, self.q_open, self.q_closed))
                # Transition to LIFT once we are in HOLD stably
                self.state = State.LIFT
                self.z_cmd = 0.0

        elif self.state == State.LIFT:        
            # Keep holding force while lifting
            if F_meas > prm.F_max:
                self.state = State.FAIL_RECOVER
                self.stable_counter = 0
            else:
                err = prm.F_des - F_meas
                dq = prm.k_force * err
                self.q_cmd = float(np.clip(self.q_cmd + dq, self.q_open, self.q_closed)) # continue force regulation
                # Advance lift
                self.z_cmd = min(prm.lift_max, self.z_cmd + prm.lift_speed)
                # Optional: stop lifting when max reached (stay in LIFT or add DONE)
                if self.z_cmd >= prm.lift_max - 1e-6:
                    self.state = State.LIFT  # or DONE

        elif self.state == State.FAIL_RECOVER:
            # Open fully then retry
            self.q_cmd = max(self.q_open, self.q_cmd - prm.emergency_open_step) # open further for recovery
            if self.q_cmd <= self.q_open + 1e-6:
                self.state = State.CLOSE_TO_CONTACT  # when fully open again, retry closing

        return self.state, self.q_cmd, self.z_cmd



