# Force-Limited Parallel Gripper in PyBullet
This repository implements a **force-limited parallel gripper** in **PyBullet**.
The system performs a **pinch-and-lift task** using physically simulated joints and a
**finite-state machine (FSM)**.

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
#### Step 5: View the PyBullet visualization:
Open a web browser and go to:
```
http://localhost:8080/vnc.html
```
You will see a Linux desktop running inside your browser.
The PyBullet GUI window should already be open and running.




! When you run the Docker the second time at the same port 8080, you will get the Error: 'Bind for 0.0.0.0:8080 failed: port is already allocated'. Do the following to free the port 8080:
- Find the process ID (PID) using port 8080 by running 
`lsof -i :8080`
- kill the process using command
`kill -9 PID`
, where, replace `PID` with the actual process ID found in the previous command.


## 2. System Design

### 2.1 Hand/Gripper Model
### 2.2 Sensing Assumptions
### 2.3 Interaction Policy
### 2.4 Failure + Mitigation

Notes: README answering:
○ How to run the code
○ What you built and why it matters for an MVP
○ System architecture and assumptions
○ Where AI is used (or why not)
○ Failure mode and safety considerations








