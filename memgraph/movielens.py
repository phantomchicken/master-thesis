import mgclient
import time

# Delete with match (n) detach delete (n);

# Connection to Memgraph
conn = mgclient.connect(host='127.0.0.1', port=7877)
cursor = conn.cursor()

# Cypher queries for loading CSV files
queries = [
    """
    LOAD CSV FROM '/var/lib/memgraph/movies.csv' 
    WITH HEADER DELIMITER '%'
    AS row
    CREATE (m:Movie {id: toInteger(row.movieId), title: row.title});
    """,
    """
    LOAD CSV FROM '/var/lib/memgraph/users.csv' 
    WITH HEADER DELIMITER ','
    AS row
    CREATE (u:User {id: toInteger(row.userId)});
    """,
    """
    LOAD CSV FROM '/var/lib/memgraph/genres.csv' 
    WITH HEADER DELIMITER ','
    AS row
    CREATE (g:Genre {id: toInteger(row.genreId), name: row.name});
    """,
    """
    LOAD CSV FROM '/var/lib/memgraph/tags.csv' 
    WITH HEADER DELIMITER '|'
    AS row
    MATCH (u:User {id: toInteger(row.userId)}), (m:Movie {id: toInteger(row.movieId)})
    CREATE (u)-[:TAGGED {tag: row.tag, timestamp: toInteger(row.timestamp)}]->(m);
    """,
    """
    LOAD CSV FROM '/var/lib/memgraph/movie_genre_edges.csv' 
    WITH HEADER DELIMITER ','
    AS row
    MATCH (m:Movie {id: toInteger(row.movieId)}), (g:Genre {id: toInteger(row.genreId)})
    CREATE (m)-[:HAS_GENRE]->(g);
    """
]

# Load the ratings files: ratings00.csv to ratings10.csv
for i in range(11):
    file_name = f"/var/lib/memgraph/ratings{str(i).zfill(2)}.csv"
    query = f"""
    LOAD CSV FROM '{file_name}' 
    WITH HEADER DELIMITER '|'
    AS row
    MATCH (u:User {{id: toInteger(row.userId)}}), (m:Movie {{id: toInteger(row.movieId)}})
    CREATE (u)-[:RATED {{rating: toFloat(row.rating), timestamp: toInteger(row.timestamp)}}]->(m);
    """
    queries.append(query)

# Start measuring total time
total_start_time = time.time()

for i, query in enumerate(queries):
    first_line = query.split('\n', 1)[0]  # Extract the first line of the query
    print(f"Executing Query {i}: {first_line}")
    cursor.execute(query)
    conn.commit()

# End measuring total time
total_end_time = time.time()
total_elapsed_time = total_end_time - total_start_time

cursor.close()
conn.close()

print(f"Data imported successfully! Total time: {total_elapsed_time:.2f} seconds.")
