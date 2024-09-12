docker cp circles.csv 8d8e2846215f:/var/lib/neo4j/import
docker cp users.csv 8d8e2846215f:/var/lib/neo4j/import
docker cp edges.csv 8d8e2846215f:/var/lib/neo4j/import
docker cp circle_memberships.csv 8d8e2846215f:/var/lib/neo4j/import
docker exec -it  neo4j bash -c "neo4j-admin database import full neo4j \
  --nodes=/var/lib/neo4j/import/users.csv \
  --nodes=/var/lib/neo4j/import/circles.csv \
  --relationships=/var/lib/neo4j/import/edges.csv \
  --relationships=/var/lib/neo4j/import/circle_memberships.csv \
  --skip-duplicate-nodes=true \
  --skip-bad-relationships=true \
  --verbose \
  --delimiter '\t' \
  --overwrite-destination \
"

