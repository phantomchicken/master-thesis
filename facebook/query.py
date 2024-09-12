from neo4j import GraphDatabase
import time

# Connect to Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = ""  # Replace with your actual Neo4j password
driver = GraphDatabase.driver(uri, auth=(username, password))

def test_query():
    with driver.session() as session:
        start_time = time.time()
        
        # Cypher query to count the number of nodes
        result = session.run("MATCH (u) RETURN COUNT(u) AS user_count")
        count = result.single()["user_count"]
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"User count: {count}")
        print(f"Query executed in {elapsed_time:.4f} seconds")

# Execute the test query
test_query()

# Close the driver connection
driver.close()
