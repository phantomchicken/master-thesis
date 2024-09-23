# docker exec -it neo4j sh bin/neo4j-admin database import full \
#   --delimiter="%" \
#   --nodes=Movie="/var/lib/neo4j/import/movies.csv" \
#   --nodes=User="/var/lib/neo4j/import/users.csv" \
#   --nodes=Genre="/var/lib/neo4j/import/genres.csv" \
#   --relationships=HAS_GENRE="/var/lib/neo4j/import/movie_genre_edges.csv" \
#   --relationships=TAGGED="/var/lib/neo4j/import/tags.csv" \
#   --relationships=RATED="/var/lib/neo4j/import/ratings.csv" \
#   --overwrite-destination=true \
#   --verbose=true

docker exec -it neo4j sh

neo4j-admin database import full --delimiter="%" \
--nodes=Movie="/var/lib/neo4j/import/movies.csv" \
--nodes=User="/var/lib/neo4j/import/users.csv" \
--nodes=Genre="/var/lib/neo4j/import/genres.csv" \
--relationships=HAS_GENRE="/var/lib/neo4j/import/movie_genre_edges.csv" \
--relationships=TAGGED="/var/lib/neo4j/import/tags.csv" \
--relationships=RATED="/var/lib/neo4j/import/ratings.csv" \
--overwrite-destination=true \
--verbose=true
