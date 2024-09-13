import mgclient
import csv

# Connect to Memgraph
conn = mgclient.connect(host='127.0.0.1', port=7877)
conn.autocommit = True
cursor = conn.cursor()

# Clear existing data
cursor.execute("MATCH (n) DETACH DELETE n;")

# Create index on :User(id)
cursor.execute("CREATE INDEX ON :User(id);")

# Function to load users from CSV and insert into Memgraph using UNWIND
def load_nodes_bulk(csv_file, batch_size=1000):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        batch = []
        for row_number, row in enumerate(reader, start=1):
            # Append each user as a list of properties
            batch.append([row['userId:ID(User)']])
            
            if len(batch) >= batch_size:
                query = """
                UNWIND $batch AS row
                CREATE (:User {id: row[0]});
                """
                cursor.execute(query, {"batch": batch})
                batch = []  # Reset the batch after execution

            if row_number % batch_size == 0:
                print(f"Processed {row_number} users...")

        # Process any remaining users
        if batch:
            query = """
            UNWIND $batch AS row
            CREATE (:User {id: row[0]});
            """
            cursor.execute(query, {"batch": batch})
            print(f"Processed {row_number} users...")

# Function to load edges from CSV and insert relationships into Memgraph using UNWIND
def load_edges(csv_file, batch_size=1000):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        batch = []
        for row_number, row in enumerate(reader, start=1):
            # Append a list of start and end IDs for UNWIND
            batch.append([row[':START_ID(User)'], row[':END_ID(User)']])
            
            if len(batch) >= batch_size:
                query = """
                UNWIND $batch AS pair
                MATCH (a:User {id: pair[0]}), (b:User {id: pair[1]})
                CREATE (a)-[:FRIENDS_WITH]->(b);
                """
                cursor.execute(query, {"batch": batch})
                batch = []  # Reset the batch after execution

            if row_number % batch_size == 0:
                print(f"Processed {row_number} edges...")

        # Process any remaining rows
        if batch:
            query = """
            UNWIND $batch AS pair
            MATCH (a:User {id: pair[0]}), (b:User {id: pair[1]})
            CREATE (a)-[:FRIENDS_WITH]->(b);
            """
            cursor.execute(query, {"batch": batch})
            print(f"Processed {row_number} edges...")

# Load the nodes and relationships
csv_users_file = r'C:\Users\Administrator\Documents\faks\magistrska\master-thesis\memgraph\users.csv'
csv_edges_file = r'C:\Users\Administrator\Documents\faks\magistrska\master-thesis\memgraph\edges.csv'

# Load users (nodes) in bulk
load_nodes_bulk(csv_users_file)

# Load friendships (edges) in bulk
load_edges(csv_edges_file)

# Close the connection
cursor.close()
conn.close()

print("Data loaded successfully!")
