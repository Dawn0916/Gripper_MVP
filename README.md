# Gripper_MVP
Gripper_MVP: Force-limited pinch

# ###### Create a conda environment and install PyBullet (conda-forge)

## In VS Code terminal (or macOS Terminal):
conda create -n pb python=3.12 -y
conda env create -f environment.yml

## Activate conda Environment:
source /opt/homebrew/Caskroom/miniforge/base/bin/activate pb

## Download dependencies: ???? 
conda install -c conda-forge pybullet numpy -y

## Run the code:
python main.py

# #################### Docker
## Download Docker from 
https://www.docker.com/products/docker-desktop/

Install Docker

## Builder docker:
<!-- docker build --no-cache -t gripper-sim . -->
docker build -t gripper-sim-vnc .


## Run docker 
<!-- docker run --rm gripper-sim
docker run --rm gripper-sim-vnc -->
docker run --rm -p 8080:8080 gripper-sim-vnc

##  Find the process ID (PID) using port 8080
lsof -i :8080
## kill the process
kill -9 PID
Replace PID with the actual process ID found in the previous command.

# Watch the output. You should see lines like:
- go to broswer http://localhost:8080
- click on vnc.html
- you will see 'noVNC connect', here click 'connect' button


