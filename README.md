# Master-thesis: Selecting a graph database

Change to datasets folder
run preprocess.sh (downloads the dataset and preprocesses the data)
run preprocessneo.sh (prepares dataset for neo4j)

## Memgraph
Change to memgraph folder
run memgraph.sh (starts container and copies data, or start and copy by yourself)
run movielens.py

## Neo4j
Change to neo4j folder
```
docker exec -it sh
neo4j-admin database import full --delimiter="%" \
--nodes=Movie="/var/lib/neo4j/import/movies.csv" \
--nodes=User="/var/lib/neo4j/import/users.csv" \
--nodes=Genre="/var/lib/neo4j/import/genres.csv" \
--relationships=HAS_GENRE="/var/lib/neo4j/import/movie_genre_edges.csv" \
--relationships=TAGGED="/var/lib/neo4j/import/tags.csv" \
--relationships=RATED="/var/lib/neo4j/import/ratings.csv" \
--overwrite-destination=true \
--verbose=true
```

## TigerGraph
Change to tigergraph folder