# Small, fast conda-compatible base
FROM mambaorg/micromamba:1.5.8

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Workdir
WORKDIR /app


# Install OS libs that PyBullet often needs (OpenGL-related) and for GUI support.
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    xfce4 xfce4-terminal dbus-x11 \
    xvfb x11vnc \
    novnc websockify \
    libgl1 libglib2.0-0 \
    xauth x11-xserver-utils \
 && rm -rf /var/lib/apt/lists/*
USER $MAMBA_USER

# Copy only environment first (better caching)
COPY environment.docker.yml /app/environment.docker.yml

# Create conda env from environment.docker.yml
RUN micromamba env create -f /app/environment.docker.yml -y && \
    micromamba clean --all --yes

# Make the env the default for subsequent RUN/CMD
ARG ENV_NAME=pb
ENV CONDA_DEFAULT_ENV=${ENV_NAME}
ENV PATH=/opt/conda/envs/${ENV_NAME}/bin:$PATH

# Copy the rest of your code
COPY . /app

# noVNC port 
EXPOSE 8080

# Run GUI mode inside container
ENV PYBULLET_GUI=1
ENV DISPLAY=:1

# Start desktop + VNC + noVNC, then run your program
COPY --chmod=755 start.sh /app/start.sh

CMD ["/app/start.sh"]

