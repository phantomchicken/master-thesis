import pyTigerGraph as tg
import pandas as pd

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

    def load_movies(self, movies_csv_path):
        # Define the loading job for movies
        self.conn.gsql("USE GRAPH movielens DROP JOB load_movies")
        movie_loading_job = f"""
        USE GRAPH movielens
        CREATE LOADING JOB load_movies FOR GRAPH {self.conn.graphname} {{
            DEFINE FILENAME movies_file="{movies_csv_path}";
            LOAD movies_file TO VERTEX Movie VALUES ($0, $1, $2) USING SEPARATOR=",st";
        }}"""
        # Create and run the loading job for movies
        self.conn.gsql(movie_loading_job)
        self.conn.gsql(f'USE GRAPH movielens RUN LOADING JOB load_movies')
        print(f"Movies loaded from {movies_csv_path}.")
    
    def load_movie_genre_edges(self, movies_csv_path):
        # Load genres from movies.csv
        movies_df = pd.read_csv(movies_csv_path)
        
        # Insert HAS_GENRE edges between movies and genres
        for _, row in movies_df.iterrows():
            movie_id = row['movieId']
            genres = row['genres'].split('|')
            for genre in genres:
                self.conn.upsertEdge("Movie", movie_id, "HAS_GENRE", "Genre", genre)
        
        print(f"Movie-genre edges loaded from {movies_csv_path}.")
    
    def load_users(self, users_csv_path):
        # Load users from users.csv (preprocessed from both ratings.csv and tags.csv)
        users_df = pd.read_csv(users_csv_path, header=None, names=['userId'])
        
        # Insert users
        for _, row in users_df.iterrows():
            user_id = row['userId']
            self.insert_vertex("User", user_id, {})
        
        print(f"Users loaded from {users_csv_path}.")
    
    def load_ratings(self, ratings_csv_path):
        # Load ratings from ratings.csv
        ratings_df = pd.read_csv(ratings_csv_path)
        
        # Insert RATED edges
        for _, row in ratings_df.iterrows():
            user_id = row['userId']
            movie_id = row['movieId']
            rating = row['rating']
            self.conn.upsertEdge("User", user_id, "RATED", "Movie", movie_id, {"rating": rating})
        
        print(f"Ratings loaded from {ratings_csv_path}.")
    
    def load_tags(self, tags_csv_path):
        # Load tags from tags.csv
        tags_df = pd.read_csv(tags_csv_path)
        
        # Insert TAGGED edges
        for _, row in tags_df.iterrows():
            user_id = row['userId']
            movie_id = row['movieId']
            tag = row['tag']
            self.conn.upsertEdge("User", user_id, "TAGGED", "Movie", movie_id, {"tag": tag})
        
        print(f"Tags loaded from {tags_csv_path}.")
        

# Initialize TigerGraphCommands with your TigerGraph instance details
tigergraph_client = TigerGraphCommands(host="http://localhost", graphname="movielens", username="tigergraph", password="tigergraph")

# Check schema
#results = TigerGraphCommands.getSchema(self=tigergraph_client)
#print(results)

movies_csv_path = r"../datasets/ml-32m/movies.csv"
genres_csv_path = r"../datasets/ml-32m/genres.csv"
users_csv_path = r"../datasets/ml-32m/users.csv"
ratings_csv_path = r"../datasets/ml-32m/ratings.csv"
tags_csv_path = r"../datasets/ml-32m/tags.csv"

# Load movies, genres, users, ratings, and tags
# tigergraph_client.load_movies(movies_csv_path)
# tigergraph_client.load_genres(genres_csv_path)
tigergraph_client.load_movie_genre_edges(movies_csv_path)
# tigergraph_client.load_users(users_csv_path)
# tigergraph_client.load_ratings(ratings_csv_path)
# tigergraph_client.load_tags(tags_csv_path)
