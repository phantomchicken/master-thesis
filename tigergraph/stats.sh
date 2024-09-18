#!/bin/bash

# Define the output file
output_file="tmp.txt"

# Start docker stats in the background and stream CPU and memory usage to a file
docker stats --format "{{.CPUPerc}}, {{.MemUsage}}" > "$output_file" &

sleep 0.5
# Get the PID of the docker stats process
DOCKER_PID=$(ps | grep "docker" | awk {'print $2'})

# Sleep for 2 seconds
sleep 2

#echo $DOCKER_PID # increment by 4 to get the correct PID

ADJUSTED_PID=$((DOCKER_PID + 4))

#echo "Adjusted PID: $ADJUSTED_PID"
# Kill the docker stats process using the found PID
kill $ADJUSTED_PID 2>/dev/null

# Wait for the process to fully terminate (optional)
#wait $ADJUSTED_PID 2>/dev/null
sed -i 's/^.......//' "$output_file"
sed -i 's/%//g; s/GiB \/.*//g' "$output_file"

#echo "Docker stats saved to $output_file"
