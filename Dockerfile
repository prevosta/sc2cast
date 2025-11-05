# SC2Cast Docker Environment
# Sprint 1.1: Minimal setup with SC2 + CUDA + Python

FROM nvidia/cuda:12.2.0-base-ubuntu22.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    python3.11 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Create symlink for python command
RUN ln -s /usr/bin/python3.11 /usr/bin/python

# Download and install StarCraft II Linux client
WORKDIR /opt
RUN wget -q http://blzdistsc2-a.akamaihd.net/Linux/SC2.4.10.zip \
    && unzip -P iagreetotheeula SC2.4.10.zip \
    && rm SC2.4.10.zip

# Set SC2 environment variable
ENV SC2PATH=/opt/StarCraftII

# Install Python packages
RUN pip install --no-cache-dir --upgrade sc2reader

# Set working directory
WORKDIR /workspace

# Default command (for testing)
CMD ["/bin/bash"]
