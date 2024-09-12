#docker exec -it neo4j bash -c "neo4j-admin database import full neo4j --nodes=/var/lib/neo4j/import/movies.csv --nodes=/var/lib/neo4j/import/actors.csv --relationships=/var/lib/neo4j/import/roles.csv
docker exec -it neo4j bash -c "
  neo4j-admin database import full neo4j \
  --nodes=/var/lib/neo4j/import/movies.csv \
  --nodes=/var/lib/neo4j/import/actors.csv \
  --relationships=/var/lib/neo4j/import/roles.csv \
  --overwrite-destination \
  --verbose \
  "