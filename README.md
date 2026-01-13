# Gripper_MVP
Gripper_MVP: Force-limited pinch

## Create a conda environment and install PyBullet (conda-forge)

In VS Code terminal (or macOS Terminal):
conda create -n pb python=3.12 -y

Activate conda Environment:
source /opt/homebrew/Caskroom/miniforge/base/bin/activate pb

Download dependencies:
conda install -c conda-forge pybullet numpy -y

# #################### Docker
# Download Docker from 
https://www.docker.com/products/docker-desktop/

Install Docker

# Builder docker:
docker build --no-cache -t gripper-sim .

# Run docker 