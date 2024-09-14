import mgclient
import csv

# Connect to Memgraph
conn = mgclient.connect(host='127.0.0.1', port=7877)
conn.autocommit = True
cursor = conn.cursor()

# Clear existing data
cursor.execute("MATCH (n) DETACH DELETE n;")

# Create indexes
cursor.execute("CREATE INDEX ON :User(id);")
cursor.execute("CREATE INDEX ON :Movie(id);")
cursor.execute("CREATE INDEX ON :Genre(name);")

# Function to load users
def load_users(csv_file, batch_size=1000):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file, delimiter='::')
        batch = []
        for row_number, row in enumerate(reader, start=1):
            batch.append([row['userId']])
            
            if len(batch) >= batch_size:
                query = """
                UNWIND $batch AS row
                CREATE (:User {id: row[0]});
                """
                cursor.execute(query, {"batch": batch})
                batch = []
            
            if row_number % batch_size == 0:
                print(f"Processed {row_number} users...")

        if batch:
            query = """
            UNWIND $batch AS row
            CREATE (:User {id: row[0]});
            """
            cursor.execute(query, {"batch": batch})
            print(f"Processed {row_number} users...")

# Function to load movies and genres
def load_movies_and_genres(csv_file, batch_size=1000):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file, delimiter='::')
        batch = []
        for row_number, row in enumerate(reader, start=1):
            genres = row['genres'].split('|')
            batch.append([row['movieId'], row['title'], genres])

            if len(batch) >= batch_size:
                query = """
                UNWIND $batch AS row
                CREATE (m:Movie {id: row[0], title: row[1]})
                WITH m, row
                UNWIND row[2] AS genre
                MERGE (g:Genre {name: genre})
                CREATE (m)-[:IN_GENRE]->(g);
                """
                cursor.execute(query, {"batch": batch})
                batch = []
            
            if row_number % batch_size == 0:
                print(f"Processed {row_number} movies...")

        if batch:
            query = """
            UNWIND $batch AS row
            CREATE (m:Movie {id: row[0], title: row[1]})
            WITH m, row
            UNWIND row[2] AS genre
            MERGE (g:Genre {name: genre})
            CREATE (m)-[:IN_GENRE]->(g);
            """
            cursor.execute(query, {"batch": batch})
            print(f"Processed {row_number} movies...")

# Function to load ratings
def load_ratings(csv_file, batch_size=1000):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file, delimiter='::')
        batch = []
        for row_number, row in enumerate(reader, start=1):
            batch.append([row['userId'], row['movieId'], row['rating']])

            if len(batch) >= batch_size:
                query = """
                UNWIND $batch AS row
                MATCH (u:User {id: row[0]}), (m:Movie {id: row[1]})
                CREATE (u)-[:RATED {rating: toFloat(row[2])}]->(m);
                """
                cursor.execute(query, {"batch": batch})
                batch = []
            
            if row_number % batch_size == 0:
                print(f"Processed {row_number} ratings...")

        if batch:
            query = """
            UNWIND $batch AS row
            MATCH (u:User {id: row[0]}), (m:Movie {id: row[1]})
            CREATE (u)-[:RATED {rating: toFloat(row[2])}]->(m);
            """
            cursor.execute(query, {"batch": batch})
            print(f"Processed {row_number} ratings...")

# Function to load tags
def load_tags(csv_file, batch_size=1000):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file, delimiter='::')
        batch = []
        for row_number, row in enumerate(reader, start=1):
            batch.append([row['userId'], row['movieId'], row['tag']])

            if len(batch) >= batch_size:
                query = """
                UNWIND $batch AS row
                MATCH (u:User {id: row[0]}), (m:Movie {id: row[1]})
                CREATE (u)-[:TAGGED {tag: row[2]}]->(m);
                """
                cursor.execute(query, {"batch": batch})
                batch = []
            
            if row_number % batch_size == 0:
                print(f"Processed {row_number} tags...")

        if batch:
            query = """
            UNWIND $batch AS row
            MATCH (u:User {id: row[0]}), (m:Movie {id: row[1]})
            CREATE (u)-[:TAGGED {tag: row[2]}]->(m);
            """
            cursor.execute(query, {"batch": batch})
            print(f"Processed {row_number} tags...")

# File paths
csv_users_file = 'users.csv'
csv_movies_file = 'movies.csv'
csv_ratings_file = 'ratings.csv'
csv_tags_file = 'tags.csv'

# Load data
load_users(csv_users_file)
load_movies_and_genres(csv_movies_file)
load_ratings(csv_ratings_file)
load_tags(csv_tags_file)

# Close the connection
cursor.close()
conn.close()

print("Data loaded successfully!")
