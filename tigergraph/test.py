import pyTigerGraph as tg
import time
import csv
import subprocess
import os

# Sample query
query = """
INTERPRET QUERY () FOR GRAPH movielenssmall SYNTAX v2 {
    FLOAT maxIter = 20;
    FLOAT damping = 0.85;

    SumAccum<FLOAT> @pr;

    // Perform PageRank calculation
    PageRank = SELECT m FROM Movie:m
        ACCUM m.@pr += damping * (m.@pr / maxIter) 
        POST-ACCUM m.@pr = (1 - damping) / maxIter;

    PRINT PageRank;
}
"""

paramsBetweenness = {
    "v_type_set": ["Movie"],               # Set of vertex types (e.g., "Movie")
    "e_type_set": ["RATED"],               # Set of edge types (e.g., "RATED")
    "reverse_e_type": ["RATED"],           # Reverse edge type (same as edge types for undirected graph)
    "max_hops": 10,                        # Max number of hops (e.g., 10)
    "top_k": 10,                           # Top K vertices to return (e.g., 10)
    "print_results": True,                 # Print results (True or False)
    "result_attribute": "",                # Optional: Specify a vertex attribute to store the results
    "file_path": "",                       # Optional: Specify a file path to save the results
    "display_edges": False                 # Whether to display edges in the output
}

paramsLouvain = {
    "v_type_set": ["User", "Movie", "Genre"],    # List of vertex types
    "e_type_set": ["RATED", "TAGGED", "HAS_GENRE"],  # List of edge types
    "weight_attribute": "RATED",               # Edge attribute for weights (use "" for unweighted)
    "maximum_iteration": 10,                   # Maximum iterations
    "result_attribute": "",                 # Attribute to store community IDs
    "file_path": "",                           # Optional: Path to save results (leave blank to skip)
    "print_stats": True                        # Whether to print execution stats
}

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
                cpu_value = float(cpu.strip('%'))*0.25
                mem_value = float(mem.split("GiB")[0])
                total_cpu += cpu_value
                total_mem += mem_value
                count += 1

    # Calculate averages
    avg_cpu = total_cpu / count if count > 0 else 0
    avg_mem = total_mem / count if count > 0 else 0
    return avg_cpu, avg_mem

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
    #conn.runInstalledQuery("tg_betweenness_cent", params=paramsBetweenness)
    conn.runInstalledQuery("tg_louvain", params=paramsLouvain)
    #conn.runInterpretedQuery(query)

    # Measure time after query execution
    end_time = time.time()
    execution_time = end_time - start_time

    # Stop Docker stats monitoring
    if os.stat(docker_stats_file).st_size == 0:
        time.sleep (0.5)
    stop_docker_stats(docker_process)

    # Clean Docker stats and calculate averages
    avg_cpu, avg_mem = clean_and_average_docker_stats(docker_stats_file)

    # Print and save results
    print(f"{query_name}: Time = {execution_time:.4f} sec, Avg CPU Usage = {avg_cpu:.2f}%, Avg RAM Usage = {avg_mem:.3f} GiB")

    # Write the result to a CSV file with numeric values only
    with open('res.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([execution_time, avg_cpu, avg_mem])

# Define the container name
container_name = "tigergraph"

# Run the query with Docker stats measurement
run_query_with_stats(query, "TigerGraph Query", container_name)
