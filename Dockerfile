# Small, fast conda-compatible base
FROM mambaorg/micromamba:1.5.8

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Workdir
WORKDIR /app

# Copy only environment first (better caching)
COPY environment.yml /app/environment.yml

# Install OS libs that PyBullet often needs (OpenGL-related).
# Note: micromamba image is Debian/Ubuntu-based.
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
 && rm -rf /var/lib/apt/lists/*
USER $MAMBA_USER

# Create conda env from environment.yml
# (Name will come from your environment.yml "name:" field)
RUN micromamba env create -f /app/environment.yml -y && \
    micromamba clean --all --yes

# Make the env the default for subsequent RUN/CMD
# If your env name is not "pb", change it here to match environment.yml
ARG ENV_NAME=pb
ENV CONDA_DEFAULT_ENV=${ENV_NAME}
ENV PATH=/opt/conda/envs/${ENV_NAME}/bin:$PATH

# Copy the rest of your code
COPY . /app

# Default: run headless (recommended in Docker on macOS)
# If your code currently forces GUI, update main.py to read PYBULLET_GUI env var.
ENV PYBULLET_GUI=0

CMD ["python", "main.py"]
