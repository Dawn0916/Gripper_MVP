#!/usr/bin/env bash
set -e

# Start a virtual X server
Xvfb :1 -screen 0 1280x720x24 -ac +extension GLX +render -noreset &
sleep 1

# Start XFCE desktop
startxfce4 &
sleep 2

# Start VNC server on display :1 (no password for local dev)
x11vnc -display :1 -forever -shared -nopw -rfbport 5900 &
sleep 1

# Start noVNC web client on port 8080
# noVNC serves a web page that connects to VNC via websockets
websockify --web=/usr/share/novnc/ 8080 localhost:5900 &
sleep 1

echo "noVNC is running: http://localhost:8080"
echo "Starting PyBullet app..."

# Run your script (must use p.GUI inside if PYBULLET_GUI=1)
python main.py
