docker  exec -it  neo4j bash -c "cd /var/lib/neo4j/import && mkdir movielens"
docker cp ../datasets/ml-32m/movies.csv neo4j:/var/lib/neo4j/import/movielens
docker cp ../datasets/ml-32m/tags.csv neo4j:/var/lib/neo4j/import/movielens
docker cp ../datasets/ml-32m/ratings.csv neo4j:/var/lib/neo4j/import/movielens
docker cp ../datasets/ml-32m/genres.csv neo4j:/var/lib/neo4j/import/movielens
docker cp ../datasets/ml-32m/users.csv neo4j:/var/lib/neo4j/import/movielens

# docker exec -it  neo4j bash -c "neo4j-admin database import full neo4j \
#   --nodes=/var/lib/neo4j/import/movielens/users.csv \
#   --nodes=/var/lib/neo4j/import/movielens/movies.csv \
#   --nodes=/var/lib/neo4j/import/movielens/genres.csv \
#   --relationships=/var/lib/neo4j/import/movielens/tags.csv \
#   --relationships=/var/lib/neo4j/import/movielens/ratings.csv \
#   --skip-duplicate-nodes=true \
#   --skip-bad-relationships=true \
#   --verbose \
#   --delimiter '\t' \
#   --overwrite-destination \
# "

#MATCH (n)
#DETACH DELETE n

#docker exec -it neo4j /bin/bash 
