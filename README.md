# Force-Limited Parallel Gripper in PyBullet
Gripper_MVP: Force-limited pinch

## Clone the code in github
```bash
git clone https://github.com/Dawn0916/Gripper_MVP.git
cd Gripper_MVP
```

## 🐳 Run with Docker + GUI
### Download and install Docker if not yet
Find Docker here: https://www.docker.com/products/docker-desktop/


### Build the Docker image:
Run the following command inside the project directory:
```bash
docker build -t gripper-sim-vnc .
```
Once the build is complete, start the container:
```bash
docker run --rm -p 8080:8080 gripper-sim-vnc
```

## View the PyBullet visualization:
Open a web browser and go to:
```
http://localhost:8080/vnc.html
```
You will see a Linux desktop running inside your browser.
The PyBullet GUI window should already be open and running.



---

When you run the Docker the second time at the same port 8080, you will get the Error: 'Bind for 0.0.0.0:8080 failed: port is already allocated'. Do the following to free the port 8080:
##  Find the process ID (PID) using port 8080
lsof -i :8080
## kill the process
kill -9 PID
Replace PID with the actual process ID found in the previous command.



# ###### Create a conda environment and install PyBullet (conda-forge)
## In VS Code terminal (or macOS Terminal):
<!-- conda create -n pb python=3.12 -y -->
conda env create -f environment.yml

## Activate conda Environment:
source /opt/homebrew/Caskroom/miniforge/base/bin/activate pb

<!-- ## Download dependencies: ???? 
conda install -c conda-forge pybullet numpy -y -->

## Run the code:
python main.py