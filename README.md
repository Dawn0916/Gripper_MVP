# Force-Limited Parallel Gripper in PyBullet
This repository implements a **force-limited parallel gripper** in **PyBullet**.
The system performs a **pinch-and-lift task** using physically simulated joints and a
**finite-state machine (FSM)**.

The goal of this project is to demonstrate a **minimal viable manipulation system (MVP)**
that emphasizes correct interaction logic, safety, and physical realism rather than
complex geometry or learning-heavy methods.

## 1. How to run the code?
#### Step 1: Clone the Repository
First, download the source code from GitHub:
```bash
git clone https://github.com/Dawn0916/Gripper_MVP.git
cd Gripper_MVP
```
#### Step 2: Install Docker 🐳 (required)
Docker is used to run the simulation in a self-contained environment, so you do not
need to install Python or PyBullet manually.
1. Download Docker Desktop from:
https://www.docker.com/products/docker-desktop/
2. Install Docker and start Docker Desktop. 
Make sure Docker is running before continuing. You can verify Docker is working by running: 
```bash
docker --version
```

#### Step 3: Build the Docker image:
Run the following command inside the project directory:
```bash
docker build -t gripper-sim-vnc .
```
#### Step 4: Run the simulation
Once the build is complete, start the container:
```bash
docker run --rm -p 8080:8080 gripper-sim-vnc
```
#### Step 5: View the PyBullet visualization (Do this ASAP after Step 4):
Open a web browser and go to:
```
http://localhost:8080/vnc.html
```
You will see a Linux desktop running inside your browser.
The PyBullet GUI window should already be open and running.

#### ⚠️ Port 8080 Already in Use?
If you see this Error: 
```nginx
Bind for 0.0.0.0:8080 failed: port is already allocated.
```
Free the port by running:
```bash
lsof -i :8080
kill -9 PID
```
Replace `PID` with the actual process ID found in the previous command.


## 2. What was built and why it matters for an MVP
This project implements a minimal force-controlled manipulation system consisting of:
- A parallel gripper with two fingers (jaws)
- A vertical lift joint
- A simple object (box)
- A finite-state machine for control

Why this matters for an MVP:
- It demonstrates core manipulation skills (pinch, force regulation, lifting)
- It avoids unnecessary complexity (full robot arm, perception stack, learning models)
- The same control structure can later scale to more complex robots or real hardware
The MVP focuses on interaction correctness rather than appearance.


## 3. System Architecture and Assumptions
### 3.1 Hand/Gripper Model
- The gripper is modeled as a PyBullet multibody:
    - One fixed anchor (base)
    - Two prismatic jaw joints (parallel closing motion)
    - One prismatic lift joint (vertical motion)

- Jaw motion is symmetric, creating a parallel pinch
- All motions are physically simulated (no teleportation)

### 3.2 Sensing Assumptions
- No vision or tactile sensors are used
- Contact force is estimated indirectly using PyBullet contact normals
- The summed normal forces on fingertip links serve as a force proxy
- This is a common assumption in simulation and early-stage controllers
### 3.3 Interaction Policy
The interaction logic is implemented as a Finite State Machine (FSM):

States include:
- CLOSE_TO_CONTACT: slowly close until contact is detected
- FORCE_REGULATE: regulate pinch force toward a desired target
- HOLD: maintain a stable grasp
- LIFT: lift the object vertically while maintaining force
- FAIL_RECOVER: open and retry if excessive force is detected

This explicit FSM design:
- Is easy to debug and reason about
- Makes safety and failure handling explicit
- Is well-suited for MVP systems and real-world robotics

## 4. Failure Modes and Safety Considerations
### Failure Mode: Excessive Force
A key failure mode in manipulation is applying too much force, which can:
- Damage the object
- Cause unstable contacts
- Lead to unrealistic simulation behavior
  
In this project, the Failure Mode was implemented by setting a lower desired force and a lower max allowed force threshold:
- `F_des: float = 6.0`
- `F_max: float = 10.0`
      
Later, the Failure-free settings are:
- `F_des: float = 80.0`
- `F_max: float = 90.0`

### Safety Measures Implemented
- Hard force cap (F_max) enforced in the FSM
- Jaw motors have a maximum allowable force
- If measured force exceeds F_max:
    - The system immediately transitions to FAIL_RECOVER
    - Jaws open to release pressure
    - The grasp attempt restarts

These safety mechanisms ensure:
- The gripper never applies unbounded force
- Failures are handled gracefully
- The behavior is closer to what would be required on real hardware


## 5. Where AI is used (or why not)?
No machine learning or AI models are used in this project.
This is a deliberate design choice:
- The task can be solved reliably with classical control and state machines
- Using AI would add complexity without improving safety or interpretability
- For an MVP, deterministic behavior and explainability are preferred
The FSM structure could later be augmented with learning-based components
(e.g., learned force targets or grasp selection), but this is outside the scope here.




## Demo Videos

### Pinch +  Lift
Picture:

<img width="733" height="373" alt="image" src="https://github.com/user-attachments/assets/a8167d4b-4fb5-49e2-babd-7a8f73d80ebb" />

Video:
https://github.com/user-attachments/assets/e99bb258-ce0f-4349-af72-3eecb46a7d49


### Failure + Mitigation
Picture:

<img width="733" height="373" alt="image" src="https://github.com/user-attachments/assets/2a39f994-08e6-4c69-af4f-f9b46c2945ad" />

Video:
https://github.com/user-attachments/assets/8fd38f8e-1932-4219-bab4-2ae768c99913





