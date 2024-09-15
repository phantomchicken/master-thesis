import csv
from neo4j import GraphDatabase

class MovieLensBatchImporter:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()

    def create_indexes(self):
        with self.driver.session() as session:
            # Create necessary indexes
            session.run("CREATE INDEX IF NOT EXISTS FOR (m:Movie) ON (m.movieId)")
            session.run("CREATE INDEX IF NOT EXISTS FOR (g:Genre) ON (g.name)")
            session.run("CREATE INDEX IF NOT EXISTS FOR (u:User) ON (u.userId)")
            print("Indexes created (if not already existing).")

    def batch_execute_unwind(self, query, data_list, batch_size=10000, current_progress=0):
        with self.driver.session() as session:
            for i in range(0, len(data_list), batch_size):
                batch_data = data_list[i:i+batch_size]
                session.run(query, {"rows": batch_data})
                current_progress += len(batch_data)
                print(f"Processed {current_progress} records.")

    def load_movies(self, movies_csv, batch_size=10000):
        with open(movies_csv, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter="%")
            data = []
            current_progress = 0
            query = """
                    UNWIND $rows AS row
                    CREATE (m:Movie {movieId: row.movieId, title: row.title})
                    """
            for row in reader:
                data.append({"title": row['title'], "movieId": row['movieId']})
                if len(data) % batch_size == 0:
                    
                    self.batch_execute_unwind(query, data, batch_size, current_progress)
                    current_progress += len(data)
                    data = []

            if data:
                self.batch_execute_unwind(query, data, batch_size, current_progress)
                
        print(f"Movies loaded from {movies_csv}")

    def load_genres(self, genres_csv, batch_size=10000):
        with open(genres_csv, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            data = []
            current_progress = 0
            query = """
            UNWIND $rows AS row
            CREATE (g:Genre {name: row.genre})
            """
            for row in reader:
                data.append({"genre": row[0]})
                
                if len(data) % batch_size == 0:
                    self.batch_execute_unwind(query, data, batch_size, current_progress)
                    current_progress += len(data)
                    data = []

            if data:  # Ensure to process the last batch if it's smaller than batch_size
                self.batch_execute_unwind(query, data, batch_size, current_progress)
                
        print(f"Genres loaded from {genres_csv}")

    def load_movie_genre_relationships(self, movies_csv, batch_size=10000):
        with open(movies_csv, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter="%")
            data = []
            current_progress = 0
            query = """
                    UNWIND $rows AS row
                    MATCH (m:Movie {movieId: row.movieId}), (g:Genre {name: row.genre})
                    MERGE (m)-[:HAS_GENRE]->(g)
                    """
            for row in reader:
                movie_id = row['movieId']
                genres = row['genres'].split('|')
                for genre in genres:
                    data.append({"movieId": movie_id, "genre": genre})
                
                if len(data) % batch_size == 0:
                    
                    self.batch_execute_unwind(query, data, batch_size, current_progress)
                    current_progress += len(data)
                    data = []

            if data:
                self.batch_execute_unwind(query, data, batch_size, current_progress)
                
        print(f"Movie-genre relationships loaded from {movies_csv}")

    def load_users(self, users_csv, batch_size=10000):
        with open(users_csv, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            data = []
            current_progress = 0
            query = """
                    UNWIND $rows AS row
                    CREATE (u:User {userId: row.userId})
                    """
            for row in reader:
                data.append({"userId": row[0]})
                
                if len(data) % batch_size == 0:
                    
                    self.batch_execute_unwind(query, data, batch_size, current_progress)
                    current_progress += len(data)
                    data = []

            if data:
                self.batch_execute_unwind(query, data, batch_size, current_progress)
                
        print(f"Users loaded from {users_csv}")

    def load_ratings(self, ratings_csv, batch_size=100000):
        with open(ratings_csv, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter="|")
            data = []
            current_progress = 0
            query = """
                    UNWIND $rows AS row
                    MATCH (u:User {userId: row.userId}), (m:Movie {movieId: row.movieId})
                    MERGE (u)-[:RATED {rating: toFloat(row.rating)}]->(m)
                    """
            for row in reader:
                data.append({
                    "userId": row['userId'], 
                    "movieId": row['movieId'], 
                    "rating": row['rating']
                })
                
                if len(data) % batch_size == 0:
                    
                    self.batch_execute_unwind(query, data, batch_size, current_progress)
                    current_progress += len(data)
                    data = []

            if data:
                self.batch_execute_unwind(query, data, batch_size, current_progress)
                
        print(f"Ratings loaded from {ratings_csv}")

    def load_tags(self, tags_csv, batch_size=100000):
        with open(tags_csv, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter="|")
            data = []
            current_progress = 0
            query = """
                    UNWIND $rows AS row
                    MATCH (u:User {userId: row.userId}), (m:Movie {movieId: row.movieId})
                    MERGE (u)-[:TAGGED {tag: row.tag}]->(m)
                    """
            for row in reader:
                data.append({"userId": row['userId'], "movieId": row['movieId'], "tag": row['tag']})
                
                if len(data) % batch_size == 0:
                    
                    self.batch_execute_unwind(query, data, batch_size, current_progress)
                    current_progress += len(data)
                    data = []

            if data:
                self.batch_execute_unwind(query, data, batch_size, current_progress)
                
        print(f"Tags loaded from {tags_csv}")

# Initialize MovieLensBatchImporter with Neo4j connection details
neo4j_importer = MovieLensBatchImporter("bolt://localhost:7687", "neo4j", "password")

# Create indexes before importing data
neo4j_importer.create_indexes()

# Paths to CSV files
movies_csv = r"../datasets/ml-10M100K/movies.csv" # % delimiter
genres_csv = r"../datasets/ml-10M100K/genres.csv"
users_csv = r"../datasets/ml-10M100K/users.csv"
ratings_csv = r"../datasets/ml-10M100K/ratings.csv" # | delimiter
ratings_csv0 = r"../datasets/ml-10M100K/ratings00.csv" # | delimiter
ratings_csv1 = r"../datasets/ml-10M100K/ratings01.csv" # | delimiter
ratings_csv2 = r"../datasets/ml-10M100K/ratings02.csv" # | delimiter
ratings_csv3 = r"../datasets/ml-10M100K/ratings03.csv" # | delimiter
ratings_csv4 = r"../datasets/ml-10M100K/ratings04.csv" # | delimiter
ratings_csv5 = r"../datasets/ml-10M100K/ratings05.csv" # | delimiter
ratings_csv6 = r"../datasets/ml-10M100K/ratings06.csv" # | delimiter
ratings_csv7 = r"../datasets/ml-10M100K/ratings07.csv" # | delimiter
ratings_csv8 = r"../datasets/ml-10M100K/ratings08.csv" # | delimiter
ratings_csv9 = r"../datasets/ml-10M100K/ratings09.csv" # | delimiter
ratings_csv10 = r"../datasets/ml-10M100K/ratings10.csv" # | delimiter
tags_csv = r"../datasets/ml-10M100K/tags.csv" # | delimiter

# Load the data in batches using UNWIND
# neo4j_importer.load_movies(movies_csv)
# neo4j_importer.load_genres(genres_csv)
# neo4j_importer.load_movie_genre_relationships(movies_csv)
# neo4j_importer.load_users(users_csv)
neo4j_importer.load_tags(tags_csv)
#neo4j_importer.load_ratings(ratings_csv)
neo4j_importer.load_ratings(ratings_csv0)
neo4j_importer.load_ratings(ratings_csv1)
neo4j_importer.load_ratings(ratings_csv2)
neo4j_importer.load_ratings(ratings_csv3)
neo4j_importer.load_ratings(ratings_csv4)
neo4j_importer.load_ratings(ratings_csv5)
neo4j_importer.load_ratings(ratings_csv6)
neo4j_importer.load_ratings(ratings_csv7)
neo4j_importer.load_ratings(ratings_csv8)
neo4j_importer.load_ratings(ratings_csv9)
neo4j_importer.load_ratings(ratings_csv10)

# Close the connection
neo4j_importer.close()
