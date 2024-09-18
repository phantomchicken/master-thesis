import mgclient
import time
import csv
import subprocess
import os

# Connect to Memgraph
conn = mgclient.connect(host='127.0.0.1', port=7877)
conn.autocommit = True
cursor = conn.cursor()

# Sample Query (adjust as needed)
query = """
CALL community_detection.get()
YIELD node, community_id;
"""  # Modify this query to fit your testing needs

# Function to start Docker stats monitoring in the background
def start_docker_stats(output_file):
    docker_process = subprocess.Popen(
        ["docker", "stats", "--format", "{{.CPUPerc}}, {{.MemUsage}}"],
        stdout=open(output_file, "w")
    )
    return docker_process

# Function to stop Docker stats monitoring
def stop_docker_stats(docker_process):
    docker_process.terminate()
    docker_process.wait()  # Ensure the process is completely stopped

# Function to clean Docker stats output and calculate averages
def clean_and_average_docker_stats(input_file):
    total_cpu = 0
    total_mem = 0
    count = 0

    with open(input_file, "r") as f:
        for line in f:
            line = line.strip().replace('\x1b[2J\x1b[H', '').strip()  # Remove special characters
            if line:
                # Remove '%' from CPU usage and GiB from memory usage
                cpu, mem = line.split(", ")
                cpu_value = float(cpu.strip('%')) * 0.25  # Normalize CPU usage by 4 cores
                mem_value = float(mem.split("GiB")[0])
                total_cpu += cpu_value
                total_mem += mem_value
                count += 1

    # Calculate averages
    avg_cpu = total_cpu / count if count > 0 else 0
    avg_mem = total_mem / count if count > 0 else 0
    return avg_cpu, avg_mem

def run_query_with_stats(query, query_name, container_name):
    # Start Docker stats monitoring
    docker_stats_file = "tmp.txt"
    docker_process = start_docker_stats(docker_stats_file)

    # Measure time for query execution
    start_time = time.time()

    # Execute the query
    cursor.execute(query)
    results = cursor.fetchall()  # Fetch the results (optional, adjust based on query)

    # Measure time after query execution
    end_time = time.time()
    execution_time = end_time - start_time

    # Stop Docker stats monitoring
    if os.stat(docker_stats_file).st_size == 0:
        time.sleep(1)
    stop_docker_stats(docker_process)

    # Clean Docker stats and calculate averages
    avg_cpu, avg_mem = clean_and_average_docker_stats(docker_stats_file)

    # Print and save results
    print(f"{query_name}: Time = {execution_time:.4f} sec, Avg CPU Usage = {avg_cpu:.2f}%, Avg RAM Usage = {avg_mem:.3f} GiB")

    # Write the result to a CSV file with numeric values only
    with open('res.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([execution_time, avg_cpu, avg_mem])

# Define the container name for Memgraph
container_name = "memgraph"

# Run the query with Docker stats measurement
run_query_with_stats(query, "Memgraph Query", container_name)

# Close the connection
cursor.close()
conn.close()
