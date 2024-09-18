import pyTigerGraph as tg
import time
import csv
import subprocess
import os

# Sample query
query = """
INTERPRET QUERY () FOR GRAPH movielenssmall { 
    SetAccum<STRING> @@usersRated;

    UsersRated = SELECT u
        FROM User:u -(RATED)-> Movie:m
        WHERE m.title == "Toy Story (1995)"
        ACCUM @@usersRated += u.userId;

    PRINT @@usersRated;
}
"""

# Function to start Docker stats monitoring in the background
def start_docker_stats(output_file):
    docker_process = subprocess.Popen(
        ["docker", "stats", "--no-stream", "--format", "{{.CPUPerc}}, {{.MemUsage}}"],
        stdout=open(output_file, "w")
    )
    return docker_process

# Function to stop Docker stats monitoring
def stop_docker_stats(docker_process):
    docker_process.terminate()
    docker_process.wait()  # Ensure the process is completely stopped

# Function to clean Docker stats output
def clean_docker_stats(input_file, output_file):
    with open(output_file, "w") as clean_file:
        with open(input_file, "r") as f:
            for line in f:
                line = line.strip()
                # Remove '%' from CPU usage and GiB from memory usage
                cpu, mem = line.split(", ")
                cpu_value = float(cpu.strip('%'))
                mem_value = float(mem.split("GiB")[0])
                clean_file.write(f"{cpu_value}, {mem_value}\n")

# Function to run a query and measure Docker stats during the execution
def run_query_with_stats(query, query_name, container_name):
    # Start Docker stats monitoring
    docker_stats_file = "tmp.txt"
    docker_process = start_docker_stats(docker_stats_file)

    # Measure time for query execution
    start_time = time.time()

    # Connect to TigerGraph server and execute query
    conn = tg.TigerGraphConnection(host="http://localhost", graphname="movielenssmall", username="tigergraph", password="tigergraph")
    conn.apiToken = conn.getToken(conn.createSecret())
    conn.runInterpretedQuery(query)

    # Measure time after query execution
    end_time = time.time()
    execution_time = end_time - start_time

    # Stop Docker stats monitoring
    stop_docker_stats(docker_process)

    # Clean Docker stats output
    clean_docker_stats(docker_stats_file, "docker_stats_output.txt")

    # Print and save results
    print(f"{query_name}: Time = {execution_time:.4f} sec")

    # Output Docker stats to console and CSV
    with open("docker_stats_output.txt", "r") as file:
        for line in file:
            cpu, mem = line.strip().split(", ")
            print(f"Docker stats during query: CPU = {cpu}%, RAM = {mem} GiB")

            # Write the result to a CSV file
            with open('res.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([execution_time, cpu, mem])

# Define the container name
container_name = "tigergraph"

# Run the query with Docker stats measurement
run_query_with_stats(query, "TigerGraph Query", container_name)
