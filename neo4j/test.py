from neo4j import GraphDatabase
import time
import csv
import subprocess
import os

# Neo4j connection details
uri = "bolt://localhost:7687"
username = "neo4j"
password = "password"

# Connect to Neo4j
driver = GraphDatabase.driver(uri, auth=(username, password))

# Sample Query
query = """
CALL gds.louvain.stream('movieGraph')
YIELD nodeId, communityId
WITH nodeId, communityId
MATCH (n) WHERE id(n) = nodeId
WITH 
  CASE 
    WHEN labels(n)[0] = 'Movie' THEN n.title
    WHEN labels(n)[0] = 'User' THEN n.userId
    WHEN labels(n)[0] = 'Genre' THEN n.name
  END AS name_or_id, communityId
ORDER BY communityId
WITH communityId, COLLECT(name_or_id)[0..5] AS sample_per_community
UNWIND sample_per_community AS name_or_id
RETURN name_or_id, communityId
ORDER BY communityId;
"""  # Modify this query as needed

# Function to create indexes and disable caching
def setup_indexes_and_clear_cache():
    with driver.session() as session:
        # Create necessary indexes
        # session.run("CREATE INDEX IF NOT EXISTS FOR (m:Movie) ON (m.movieId)")
        # session.run("CREATE INDEX IF NOT EXISTS FOR (g:Genre) ON (g.name)")
        # session.run("CREATE INDEX IF NOT EXISTS FOR (u:User) ON (u.userId)")

        # Clear query cache
        session.run("CALL db.clearQueryCaches()")

def setup_graph():
    with driver.session() as session:
        session.run("""
            CALL gds.graph.project(
                'movieGraph',
                ['User', 'Movie','Genre'],
                {
                    RATED: {
                        type: 'RATED',
                        properties: 'rating'
                    },
                    TAGGED: {
                        type: 'TAGGED'
                    },
                    HAS_GENRE: {
                        type: 'HAS_GENRE'
                    }
                }
            )
        """)

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

# Function to run a query and measure Docker stats during the execution
def run_query_with_stats(query, query_name, container_name):
    # Start Docker stats monitoring
    docker_stats_file = "tmp.txt"
    docker_process = start_docker_stats(docker_stats_file)


    # Execute the Neo4j query
    with driver.session() as session:
        session.run("CALL db.clearQueryCaches()")
        setup_graph()
        # Measure time for query execution
        start_time = time.time()
        session.run(query)

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

# Define the container name for Neo4j
container_name = "neo4j"

# Set up indexes and clear cache
setup_indexes_and_clear_cache()

# Run the query with Docker stats measurement
run_query_with_stats(query, "Neo4j Query", container_name)

# Close the Neo4j connection
driver.close()
