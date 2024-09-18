import mgclient

# fix lines 9812 in movies remove double quotes in great performances and 9/11
# make sure to copy .csv files to /var/lib/memgraph
# remove " from tagsmemgraph.csv

# Connection to Memgraph
conn = mgclient.connect(host='127.0.0.1', port=7877)
cursor = conn.cursor()

# Cypher queries for loading CSV files
queries = [
    # """
    # LOAD CSV FROM '/var/lib/memgraph/moviesmemgraph.csv' 
    # WITH HEADER DELIMITER '%'
    # AS row
    # CREATE (m:Movie {id: toInteger(row.movieId), title: row.title});
    # """,
    # """
    # LOAD CSV FROM '/var/lib/memgraph/usersmemgraph.csv' 
    # WITH HEADER DELIMITER ','
    # AS row
    # CREATE (u:User {id: toInteger(row.userId)});
    # """,
    # """
    # LOAD CSV FROM '/var/lib/memgraph/genresmemgraph.csv' 
    # WITH HEADER DELIMITER ','
    # AS row
    # CREATE (g:Genre {id: toInteger(row.genreId), name: row.name});
    # """,
    # """
    # LOAD CSV FROM '/var/lib/memgraph/tagsmemgraph.csv' 
    # WITH HEADER DELIMITER ','
    # AS row
    # MATCH (u:User {id: toInteger(row.userId)}), (m:Movie {id: toInteger(row.movieId)})
    # CREATE (u)-[:TAGGED {tag: row.tag, timestamp: toInteger(row.timestamp)}]->(m);
    # """,
    # """
    # LOAD CSV FROM '/var/lib/memgraph/ratings.csv' 
    # WITH HEADER DELIMITER '|'
    # AS row
    # MATCH (u:User {id: toInteger(row.userId)}), (m:Movie {id: toInteger(row.movieId)})
    # CREATE (u)-[:RATED {rating: toFloat(row.rating), timestamp: toInteger(row.timestamp)}]->(m);
    # """,
    # """
    # LOAD CSV FROM '/var/lib/memgraph/movie_genre_edgesmemgraph.csv' 
    # WITH HEADER DELIMITER ','
    # AS row
    # MATCH (m:Movie {id: toInteger(row.movieId)}), (g:Genre {id: toInteger(row.genreId)})
    # CREATE (m)-[:HAS_GENRE]->(g);
    # """,
    """
    LOAD CSV FROM '/var/lib/memgraph/ratings02.csv' 
    WITH HEADER DELIMITER '|'
    AS row
    MATCH (u:User {id: toInteger(row.userId)}), (m:Movie {id: toInteger(row.movieId)})
    CREATE (u)-[:RATED {rating: toFloat(row.rating), timestamp: toInteger(row.timestamp)}]->(m);
    """
]

for query in queries:
    cursor.execute(query)
    conn.commit()

cursor.close()
conn.close()

print("Data imported successfully!")
