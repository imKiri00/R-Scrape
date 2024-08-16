FROM mcr.microsoft.com/playwright:v1.46.0-jammy

# Install Python and pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set up a non-root user
RUN useradd -m user
USER user
WORKDIR /home/user

# Copy your project files
COPY --chown=user:user . /home/user/app

# Install Python dependencies
COPY --chown=user:user requirements.txt /home/user/app/
RUN pip3 install --user -r /home/user/app/requirements.txt

# Add local user bin to PATH
ENV PATH="/home/user/.local/bin:${PATH}"

# Set the display environment variable
ENV DISPLAY=:0

# Set the entry point
ENTRYPOINT ["python3", "/home/user/app/main.py"]