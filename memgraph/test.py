import mgclient
import psutil
import time
import csv
import os

# Connect to Memgraph
conn = mgclient.connect(host='127.0.0.1', port=7877)
conn.autocommit = True
cursor = conn.cursor()

# Sample Query (adjust as needed)
query = """
CALL betweenness_centrality.get(True, True) 
YIELD node, betweenness_centrality
RETURN node, betweenness_centrality
ORDER BY betweenness_centrality DESC
LIMIT 10;
"""  # Modify this query to fit your testing needs

def run_query(query, query_name):
    # Get the current process
    process = psutil.Process(os.getpid())

    # Measure time and system resource usage
    start_time = time.time()

    # Measure initial CPU and memory usage
    cpu_start = psutil.cpu_percent(interval=None)  # Get instant CPU usage
    mem_start = process.memory_info().rss / (1024 * 1024)  # Convert bytes to MB

    # Execute the query
    cursor.execute(query)
    results = cursor.fetchall()  # Fetch the results (optional, adjust based on query)

    # Measure time and system resource usage after execution
    end_time = time.time()

    # Measure CPU usage after query
    cpu_end = psutil.cpu_percent(interval=None)  # Get instant CPU usage

    # Measure memory usage after query
    mem_end = process.memory_info().rss / (1024 * 1024)

    # Calculate metrics
    execution_time = end_time - start_time
    cpu_usage = cpu_end - cpu_start if cpu_end >= cpu_start else 0   # CPU usage in percentage
    ram_usage = mem_end - mem_start if mem_end >= mem_start else 0  # Memory difference during query

    print(f"{query_name}: Time = {execution_time:.4f} sec, CPU Usage = {cpu_usage:.2f}%, RAM = {ram_usage:.2f} MB")

    # Write the result to a CSV file
    with open('res.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([execution_time, cpu_usage, ram_usage])

# Run the query once
run_query(query, "Memgraph Query")

# Close the connection
cursor.close()
conn.close()
