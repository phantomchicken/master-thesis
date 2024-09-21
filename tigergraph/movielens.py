import pyTigerGraph as tg
import time

class TigerGraphCommands:
    def __init__(self, host, graphname, username, password):
        self.conn = tg.TigerGraphConnection(host=host, graphname=graphname, username=username, password=password)
    
    def load_movies(self, movies_csv_path):
        # Define the loading job for movies
        self.conn.gsql("USE GRAPH movielens DROP JOB load_movies")
        movie_loading_job = f"""
        USE GRAPH movielens
        CREATE LOADING JOB load_movies FOR GRAPH {self.conn.graphname} {{
            DEFINE FILENAME movies_file="{movies_csv_path}";
            LOAD movies_file TO VERTEX Movie VALUES ($0, $1, $2) USING SEPARATOR="%";
        }}"""
        # Create and run the loading job for movies
        self.conn.gsql(movie_loading_job)
        self.conn.gsql(f'USE GRAPH movielens RUN LOADING JOB load_movies')
        print(f"Movies loaded from {movies_csv_path}.")
    
    def load_genres(self, genres_csv_path):
        # Define the loading job for genres
        self.conn.gsql("USE GRAPH movielens DROP JOB load_genres")
        genres_loading_job = f"""
        USE GRAPH movielens
        CREATE LOADING JOB load_genres FOR GRAPH {self.conn.graphname} {{
            DEFINE FILENAME genres_file="{genres_csv_path}";
            LOAD genres_file TO VERTEX Genre VALUES ($0, $1) USING SEPARATOR=",";
        }}"""
        # Create and run the loading job for genres
        self.conn.gsql(genres_loading_job)
        self.conn.gsql(f'USE GRAPH movielens RUN LOADING JOB load_genres')
        print(f"Genres loaded from {genres_csv_path}.")

    def load_users(self, users_csv_path):
        # Define the loading job for users
        self.conn.gsql("USE GRAPH movielens DROP JOB load_users")
        users_loading_job = f"""
        USE GRAPH movielens
        CREATE LOADING JOB load_users FOR GRAPH {self.conn.graphname} {{
            DEFINE FILENAME users_file="{users_csv_path}";
            LOAD users_file TO VERTEX User VALUES ($0) USING SEPARATOR="%";
        }}"""
        # Create and run the loading job for users
        self.conn.gsql(users_loading_job)
        self.conn.gsql(f'USE GRAPH movielens RUN LOADING JOB load_users')
        print(f"Users loaded from {users_csv_path}.")
    
    def load_ratings(self, ratings_csv_path):
        # Define the loading job for ratings
        self.conn.gsql("USE GRAPH movielens DROP JOB load_ratings")
        ratings_loading_job = f"""
        USE GRAPH movielens
        CREATE LOADING JOB load_ratings FOR GRAPH {self.conn.graphname} {{
            DEFINE FILENAME ratings_file="{ratings_csv_path}";
            LOAD ratings_file TO EDGE RATED VALUES ($0, $1, $2, $3) USING SEPARATOR="|";
        }}"""
        # Create and run the loading job for ratings
        self.conn.gsql(ratings_loading_job)
        self.conn.gsql(f'USE GRAPH movielens RUN LOADING JOB load_ratings')
        print(f"Ratings loaded from {ratings_csv_path}.")
    
    def load_tags(self, tags_csv_path):
        # Define the loading job for tags
        self.conn.gsql("USE GRAPH movielens DROP JOB load_tags")
        tags_loading_job = f"""
        USE GRAPH movielens
        CREATE LOADING JOB load_tags FOR GRAPH {self.conn.graphname} {{
            DEFINE FILENAME tags_file="{tags_csv_path}";
            LOAD tags_file TO EDGE TAGGED VALUES ($0, $1, $2, $3) USING SEPARATOR="|";
        }}"""
        # Create and run the loading job for tags
        self.conn.gsql(tags_loading_job)
        self.conn.gsql(f'USE GRAPH movielens RUN LOADING JOB load_tags')
        print(f"Tags loaded from {tags_csv_path}.")
    
    def load_movie_genre_edges(self, movie_genre_edges_csv_path):
        # Define the loading job for movie-genre edges
        self.conn.gsql("USE GRAPH movielens DROP JOB load_movie_genre_edges")
        movie_genre_edges_job = f"""
        USE GRAPH movielens
        CREATE LOADING JOB load_movie_genre_edges FOR GRAPH {self.conn.graphname} {{
            DEFINE FILENAME movie_genre_file="{movie_genre_edges_csv_path}";
            LOAD movie_genre_file TO EDGE HAS_GENRE VALUES ($0, $1) USING SEPARATOR=",";
        }}"""
        # Create and run the loading job for movie-genre edges
        self.conn.gsql(movie_genre_edges_job)
        self.conn.gsql(f'USE GRAPH movielens RUN LOADING JOB load_movie_genre_edges')
        print(f"Movie-genre edges loaded from {movie_genre_edges_csv_path}.")

# Initialize TigerGraphCommands with your TigerGraph instance details
tigergraph_client = TigerGraphCommands(host="http://localhost", graphname="movielens", username="tigergraph", password="tigergraph")

# Paths to CSV files
movies_csv_path = r"/tmp/movies.csv"
genres_csv_path = r"/tmp/genres.csv"
users_csv_path = r"/tmp/users.csv"
ratings_csv_path = r"/tmp/ratings.csv"
tags_csv_path = r"/tmp/tags.csv"
movie_genre_edges_csv_path = r"/tmp/movie_genre_edges.csv"


# Call individual loading functions
total_start_time = time.time()
tigergraph_client.load_movies(movies_csv_path)
tigergraph_client.load_genres(genres_csv_path)
tigergraph_client.load_users(users_csv_path)
tigergraph_client.load_tags(tags_csv_path)
tigergraph_client.load_movie_genre_edges(movie_genre_edges_csv_path)
tigergraph_client.load_ratings(ratings_csv_path)
total_end_time = time.time()
total_elapsed_time = total_end_time - total_start_time

print(f"Data imported successfully! Total time: {total_elapsed_time:.2f} seconds.")
