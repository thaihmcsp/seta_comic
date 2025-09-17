import os
import time
import subprocess
import sys

def run_command(command, description=None):
    """Run a command and print its output."""
    if description:
        print(f"\n{description}...")
    
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        text=True
    )
    
    # Print output in real-time
    for line in process.stdout:
        print(line, end='')
    
    process.wait()
    
    if process.returncode != 0:
        print(f"Error executing command: {command}")
        for line in process.stderr:
            print(line, end='')
        return False
    
    return True

def run_command_in_container(container_name, command, description=None):
    """Run a command inside a Docker container."""
    docker_command = f"docker exec {container_name} {command}"
    return run_command(docker_command, description)

def main():
    """Main setup function."""
    print("Setting up Seta Comic with PostgreSQL and Python app in Docker")
    
    # Check if Docker is installed
    if not run_command("docker --version", "Checking Docker installation"):
        print("Docker is not installed or not in PATH. Please install Docker and try again.")
        return
    
    # Check if Docker Compose is installed
    if not run_command("docker-compose --version", "Checking Docker Compose installation"):
        print("Docker Compose is not installed or not in PATH. Please install Docker Compose and try again.")
        return
    
    # Build and start containers
    print("\nBuilding and starting containers...")
    if not run_command("docker-compose up -d --build", "Building and starting containers"):
        print("Failed to build and start containers.")
        return
    
    # Wait for PostgreSQL to be ready
    print("\nWaiting for PostgreSQL to be ready...")
    time.sleep(10)  # Give PostgreSQL some time to start
    
    # Run Alembic migrations inside the app container
    print("\nRunning database migrations...")
    if not run_command_in_container("seta_comic_app", "alembic upgrade head", "Running database migrations"):
        print("Failed to run database migrations.")
        return
    
    # Seed the database inside the app container
    print("\nSeeding the database...")
    if not run_command_in_container("seta_comic_app", "python -m app.db.seed_data", "Seeding the database"):
        print("Failed to seed the database.")
        return
    
    print("\n✅ Setup completed successfully!")
    print("\nThe application is now running at:")
    print("  http://localhost:8000")
    print("\nTo stop the containers, run:")
    print("  docker-compose down")

if __name__ == "__main__":
    main()