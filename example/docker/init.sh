#!/bin/bash

# Step 1: Create containers from 'docker-compose.yml'
echo "Starting container creation using 'docker-compose.yml'..."

if [ ! -f ./docker-compose.yml ]; then
  echo "Error: 'docker-compose.yml' not found in the current directory."
  exit 1
fi

# Create containers
docker-compose up -d
if [ $? -ne 0 ]; then
  echo "Error: Failed to execute 'docker-compose up'. Check your docker-compose configuration."
  exit 1
fi

# Step 2: Check if containers are created successfully
echo "Checking if containers are running..."

CONTAINERS_RUNNING=$(docker ps -q)
if [ -z "$CONTAINERS_RUNNING" ]; then
  echo "Error: No containers are running after 'docker-compose up'."
  exit 1
fi

echo "Containers are running successfully."

# Step 3: SSH key exchange using ssh-copy-id
echo "Performing SSH key exchange..."

# Check if SSH keys exist, generate if they don't
if [ ! -f ~/.ssh/id_rsa ]; then
  echo "SSH key not found. Generating new SSH key..."
  ssh-keygen -t rsa -b 2048 -N "" -f ~/.ssh/id_rsa
  if [ $? -ne 0 ]; then
    echo "Error: Failed to generate SSH key."
    exit 1
  fi
fi

# Loop through running containers and perform ssh-copy-id
for container_id in $CONTAINERS_RUNNING; do
  # Extract host port bound to the container's SSH port (22)
  host_port=$(docker inspect -f '{{range $p, $conf := .NetworkSettings.Ports}} {{if eq $p "22/tcp"}}{{(index $conf 0).HostPort}}{{end}}{{end}}' $container_id)

  if [ -z "$host_port" ]; then
    echo "Error: Unable to get host port for SSH for container $container_id."
    continue
  fi

  echo "Copying SSH key to container $container_id on localhost:$host_port..."

  # Use ssh-copy-id to add SSH key to the container via localhost:host_port
  ssh-copy-id -p "$host_port" -i ~/.ssh/id_rsa.pub "root@localhost"
  if [ $? -ne 0 ]; then
    echo "Error: Failed to execute 'ssh-copy-id' for container $container_id on localhost:$host_port."
    continue
  fi

  echo "SSH key copied successfully to container $container_id on localhost:$host_port."
done

echo "Script execution completed."
