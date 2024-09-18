import pyTigerGraph as tg
import time
import csv
import subprocess
import psutil
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

# Function to get Docker stats
def get_docker_stats(container_name):
    result = subprocess.run(
        ["docker", "stats", "--no-stream", "--format", "{{.CPUPerc}}, {{.MemUsage}}"],
        stdout=subprocess.PIPE,
        text=True
    )
    stats = result.stdout.strip()
    cpu, mem = stats.split(", ")
    cpu_value = float(cpu.strip('%'))  # Remove '%' from CPU and convert to float
    mem_value = float(mem.split("GiB")[0])  # Extract memory value (before 'GiB') and convert to float
    return cpu_value, mem_value

def run_query_once(query, query_name, container_name):
    # Get Docker stats before query execution and before connection
    cpu_before, mem_before = get_docker_stats(container_name)

    # Measure time for query execution
    start_time = time.time()

    # Connect to TigerGraph server
    conn = tg.TigerGraphConnection(host="http://localhost", graphname="movielenssmall", username="tigergraph", password="tigergraph")
    conn.apiToken = conn.getToken(conn.createSecret())

    # Execute the TigerGraph query
    conn.runInterpretedQuery(query)

    # Measure time after query execution
    end_time = time.time()
    execution_time = end_time - start_time

    # Get Docker stats after query execution
    cpu_after, mem_after = get_docker_stats(container_name)

    # Print the result
    print(f"{query_name}: Time = {execution_time:.4f} sec, CPU Usage = {cpu_after:.2f}%, RAM = {mem_after:.3f} GiB")

    # Write the result to a CSV file with numeric values only
    with open('res.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([execution_time, cpu_after, mem_after])

# Define the container name (replace with your actual container name)
container_name = "tigergraph"

# Run the query once
run_query_once(query, "TigerGraph Query", container_name)
