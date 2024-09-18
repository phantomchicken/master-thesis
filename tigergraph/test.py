import pyTigerGraph as tg
import time
import psutil
import statistics
import os
import csv

# TigerGraph connection details
HOST = "http://localhost"  # Update if running elsewhere
PORT = "9000"
GRAPH_NAME = "movielenssmall"
USERNAME = "tigergraph"
PASSWORD = "tigergraph"

# Connect to TigerGraph server
conn = tg.TigerGraphConnection(host=HOST, graphname=GRAPH_NAME, username=USERNAME, password=PASSWORD)
conn.apiToken = conn.getToken(conn.createSecret())

params = {
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

# Queries
query1 = """
INTERPRET QUERY () FOR GRAPH movielenssmall { 
    SetAccum<STRING> @@usersRated;

    UsersRated = SELECT u
        FROM User:u -(RATED)-> Movie:m
        WHERE m.title == "Toy Story (1995)"
        ACCUM @@usersRated += u.userId;

    PRINT @@usersRated;
}
"""

def run_query_once(query, query_name):
    # Get the current process
    a=conn.getEndpoints(dynamic=True)
    process = psutil.Process(os.getpid())

    # Measure time and system resource usage
    start_time = time.time()

    # Measure initial CPU and memory usage
    cpu_start = psutil.cpu_percent(interval=None)
    mem_start = process.memory_info().rss / (1024 * 1024)  # Convert bytes to MB

    # Execute the query
    #conn.runInstalledQuery("tg_betweenness_cent", params=params)
    conn.runInterpretedQuery(query)

    # Measure time and system resource usage after execution
    end_time = time.time()
    cpu_end = psutil.cpu_percent(interval=None)
    mem_end = process.memory_info().rss / (1024 * 1024)

    # Calculate metrics
    execution_time = end_time - start_time
    cpu_usage = cpu_end - cpu_start if cpu_end >= cpu_start else 0   # CPU usage in percentage
    ram_usage = mem_end - mem_start if mem_end >= mem_start else 0 # Memory difference during query

    print(f"{query_name}: Time = {execution_time:.4f} sec, CPU Usage = {cpu_usage:.2f}%, RAM = {ram_usage:.2f} MB")

    # Write the result to a CSV file
    with open('res.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([execution_time, cpu_usage, ram_usage])

if __name__ == "__main__":
    run_query_once(query1, "Query")
