import pyTigerGraph as tg

# Define the connection parameters
hostName = "http://localhost"
graphName = "facebook"
userName = "tigergraph"
password = "tigergraph"
restpp_port = "9000"  # Not needed for interpreter mode, but keeping it for reference
gs_port = "14240"  # GraphStudio port for managing the graph

# Establish connection
conn = tg.TigerGraphConnection(
    host=hostName,
    graphname=graphName,
    username=userName,
    password=password,
    gsPort=gs_port,
    apiToken=""
)

# Print the connection object
print(conn)

# Authenticate to get the token
token = conn.getToken(conn.createSecret())
print(f"Token: {token}")

# Create two sample User nodes and an edge between them using GSQL interpreter mode
def create_sample_data():
    # Insert two users
    schema_creation_query = """
    CREATE VERTEX User (PRIMARY_ID id STRING, name STRING) WITH primary_id_as_attribute="true";
    CREATE UNDIRECTED EDGE FRIENDS_WITH (FROM User, TO User);
    """
    conn.gsql(schema_creation_query, options=[])

    # Insert sample data using GSQL interpreter
    insert_data_query = """
    INTERPRET QUERY () FOR GRAPH facebook {
        INSERT INTO User (PRIMARY_ID) VALUES ("1");
        INSERT INTO User (PRIMARY_ID) VALUES ("2");
    }

    """
    conn.gsql(insert_data_query)
    print("Two user nodes and an edge between them have been created.")

# Query the data using GSQL interpreter mode
def query_data():
    query = """
    USE GRAPH facebook
    INTERPRET QUERY () FOR GRAPH facebook {
        users = SELECT u FROM User:u;
        PRINT users;
    }
    """
    result = conn.gsql(query)
    print("Query Results:")
    print(result)

# Delete everything using GSQL interpreter mode
def delete_everything():
    delete_query = """
    BEGIN
    start = {User.*};
    DELETE start;
    END;
    """
    conn.gsql(delete_query)
    print("All nodes and edges have been deleted.")

# Create, query, and delete the data using GSQL interpreter mode
create_sample_data()
query_data()
#delete_everything()
