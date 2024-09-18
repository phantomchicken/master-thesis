docker exec tigergraph  //home/tigergraph/tigergraph/app/4.1.0/cmd/gsql "CREATE VERTEX User (PRIMARY_ID id UINT)"
docker exec tigergraph //home/tigergraph/tigergraph/app/4.1.0/cmd/gsql "CREATE VERTEX Movie (PRIMARY_ID id UINT, title STRING)"
docker exec tigergraph //home/tigergraph/tigergraph/app/4.1.0/cmd/gsql "CREATE VERTEX Genre (PRIMARY_ID name STRING)"

docker exec tigergraph //home/tigergraph/tigergraph/app/4.1.0/cmd/gsql "CREATE UNDIRECTED EDGE RATED (FROM User, TO Movie, rating DOUBLE, timestamp UINT)"
docker exec tigergraph //home/tigergraph/tigergraph/app/4.1.0/cmd/gsql "CREATE UNDIRECTED EDGE TAGGED (FROM User, TO Movie, tag STRING, timestamp UINT)"
docker exec tigergraph //home/tigergraph/tigergraph/app/4.1.0/cmd/gsql "CREATE UNDIRECTED EDGE HAS_GENRE (FROM Movie, TO Genre)"
docker exec tigergraph //home/tigergraph/tigergraph/app/4.1.0/cmd/gsql "CREATE GRAPH movielens(User, Movie, Genre, RATED, TAGGED, HAS_GENRE)"
docker exec tigergraph //home/tigergraph/tigergraph/app/4.1.0/cmd/gsql "INSTALL DATASET"

docker cp ../datasets/ml-32m/movies.csv tigergraph:/home/tigergraph/tigergraph/data/gsql/movies.csv
docker cp ../datasets/ml-32m/tags.csv tigergraph:/home/tigergraph/tigergraph/data/gsql/tags.csv
docker cp ../datasets/ml-32m/ratings.csv tigergraph:/home/tigergraph/tigergraph/data/gsql/ratings.csv
docker cp ../datasets/ml-32m/genres.csv tigergraph:/home/tigergraph/tigergraph/data/gsql/genres.csv
docker cp ../datasets/ml-32m/users.csv tigergraph:/home/tigergraph/tigergraph/data/gsql/users.csv

docker exec tigergraph //home/tigergraph/tigergraph/app/4.1.0/cmd/gsql "SHOW GRAPH movielens"
docker exec -it tigergraph //home/tigergraph/tigergraph/app/4.1.0/cmd/gadmin "restart gsql"


INSTALL QUERY tg_louvain
INSTALL QUERY tg_betweenness_cent
# running algorithms
#docker exec -tigergraph sh
#//home/tigergraph/tigergraph/app/4.1.0/cmd//gsql SET query_timeout=60
# gsql
# USE GRAPH movielens
# RUN QUERY tg_betweenness_cent 

# Deleting everything
#DROP USERS
#DROP EDGES
#DROP GRAPH
#DROP ALL QUERIES
#DROP ALL JOBS
# CLEAR GRAPH STORE -HARD