import pyTigerGraph as tg

class TigerGraphCommands:
    def __init__(self, host, graphname, username, password):
        self.conn = tg.TigerGraphConnection(host=host, graphname=graphname, username=username, password=password)
    
    def getSchema(self):
        return self.conn.getSchema()

    def insert_vertex(self, vertex_type, vertex_id, properties):
        # Insert vertex, passing the primary ID (vertex_id) separately
        self.conn.upsertVertex(vertex_type, vertex_id, properties)

    def insert_edge(self, from_vertex_id, to_vertex_id, edge_type, properties=None):
        if properties is None:
            properties = {}
        # Insert edge between two vertices
        self.conn.upsertEdge("User", from_vertex_id, edge_type, "User", to_vertex_id, properties)

    def find_vertex(self, vertex_type, vertex_id=None):
        # If vertex_id is provided, use it to get a specific vertex
        if vertex_id:
            return self.conn.getVerticesById(vertex_type, vertex_id)
        # Otherwise, return all vertices of the given type
        return self.conn.getVertices(vertex_type)

    def find_edge(self, from_vertex_id, to_vertex_id, edge_type):
        # Get edges between two vertices
        return self.conn.getEdges("User", from_vertex_id, edge_type)

    def update_vertex(self, vertex_type, vertex_id, update_properties):
        # Update the vertex with new properties
        self.conn.upsertVertex(vertex_type, vertex_id, update_properties)

    def delete_vertex(self, vertex_type, vertex_id):
        # Delete the vertex by ID
        self.conn.deleteVertices(vertex_type, where="PRIMARY_ID = '" + vertex_id + "'")

    def delete_edge(self, from_vertex_id, to_vertex_id, edge_type):
        # Delete the edge between two vertices
        self.conn.deleteEdges("User", from_vertex_id, edge_type, "User", to_vertex_id)

    def load_users(self, user_csv_path):
        # Define the loading job for users
        self.conn.gsql("USE GRAPH facebook DROP JOB load_users")
        user_loading_job = f"""
        USE GRAPH facebook
        CREATE LOADING JOB load_users FOR GRAPH {self.conn.graphname} {{
            DEFINE FILENAME users_file="{user_csv_path}";
            LOAD users_file TO VERTEX User VALUES ($0) USING SEPARATOR="\\t";
        }}"""
        # Create and run the loading job for users
        self.conn.gsql(user_loading_job)
        self.conn.gsql(f'USE GRAPH facebook RUN LOADING JOB load_users')
        print(f"Users loaded from {user_csv_path}.")

    def load_edges(self, edge_csv_path):
        # Define the loading job for edges
        self.conn.gsql("USE GRAPH facebook DROP JOB load_edges")
        edge_loading_job = f"""
        USE GRAPH facebook
        CREATE LOADING JOB load_edges FOR GRAPH {self.conn.graphname} {{
            DEFINE FILENAME edges_file="{edge_csv_path}";
            LOAD edges_file TO EDGE FRIENDS_WITH VALUES ($0, $1) USING SEPARATOR="\\t";
        }}"""
        # Create and run the loading job for edges
        self.conn.gsql(edge_loading_job)
        self.conn.gsql(f'USE GRAPH facebook RUN LOADING JOB load_edges')
        print(f"Edges loaded from {edge_csv_path}.")

# Initialize TigerGraphCommands with your TigerGraph instance details
tigergraph_client = TigerGraphCommands(host="http://localhost", graphname="facebook", username="tigergraph", password="tigergraph")

# Check schema
#results = TigerGraphCommands.getSchema(self=tigergraph_client)
#print(results)

#tigergraph_client.insert_vertex("User", "3", {}) #tigergraph_client.insert_vertex("User", "4", {})
#tigergraph_client.insert_edge(from_vertex_id="3", to_vertex_id="4", edge_type="FRIENDS_WITH")

#u = tigergraph_client.find_vertex("User", vertex_id="3")
#friends_edges = tigergraph_client.find_edge("3", "4", "FRIENDS_WITH")

#print("Found user:", u)
#print("Found edges:", friends_edges)

# Paths to your CSV files
user_csv_path = r"~/tigergraph/data/gsql/users.csv"
edge_csv_path = r"~/tigergraph/data/gsql/edges.csv"


# Load users and edges
tigergraph_client.load_users(user_csv_path)
tigergraph_client.load_edges(edge_csv_path)

