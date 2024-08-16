import streamlit as st
import docker
import subprocess
import os
import time

def show():
    st.header("Docker Container Management")
    
    client = docker.from_env()
    
    st.subheader("Running Containers")
    containers = client.containers.list()
    for container in containers:
        st.write(f"Container ID: {container.short_id}, Name: {container.name}, Status: {container.status}")
    
    st.subheader("Docker Compose Management")
    
    # Create an empty element to update for terminal-like output
    terminal_output = st.empty()

    def update_terminal(process):
        output = []
        for line in iter(process.stdout.readline, ''):
            output.append(line.strip())
            terminal_output.code('\n'.join(output[-20:]))  # Show last 20 lines
            time.sleep(0.1)

    def run_docker_compose_command(command):
        try:
            original_dir = os.getcwd()
            
            # Check if "Playwright" directory exists
            if os.path.isdir("Playwright"):
                os.chdir("Playwright")
                st.info("Changed to Playwright directory.")
            else:
                st.info("Already in the correct directory or Playwright directory not found.")
            
            # Run docker-compose command
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            update_terminal(process)

            # Wait for the process to complete
            process.wait()
            
            if process.returncode == 0:
                st.success(f"docker-compose {command[1]} completed successfully.")
            else:
                st.error(f"Error running docker-compose {command[1]}.")
            
            # Change back to the original directory
            os.chdir(original_dir)
            st.info("Changed back to the original directory.")
        except Exception as e:
            st.error(f"Error running docker-compose {command[1]}: {str(e)}")

    if st.button("Run docker-compose"):
        run_docker_compose_command(["docker-compose", "up", "-d"])
    
    if st.button("Stop docker-compose"):
        run_docker_compose_command(["docker-compose", "down"])

    if st.button("View docker-compose logs"):
        run_docker_compose_command(["docker-compose", "logs"])