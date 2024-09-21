docker exec tigergraph  //home/tigergraph/tigergraph/app/4.1.0/cmd/gsql "CREATE VERTEX User (PRIMARY_ID id UINT)"
docker exec tigergraph //home/tigergraph/tigergraph/app/4.1.0/cmd/gsql "CREATE VERTEX Movie (PRIMARY_ID id UINT, title STRING)"
docker exec tigergraph //home/tigergraph/tigergraph/app/4.1.0/cmd/gsql "CREATE VERTEX Genre (PRIMARY_ID name STRING)"

docker exec tigergraph //home/tigergraph/tigergraph/app/4.1.0/cmd/gsql "CREATE UNDIRECTED EDGE RATED (FROM User, TO Movie, rating DOUBLE, timestamp UINT)"
docker exec tigergraph //home/tigergraph/tigergraph/app/4.1.0/cmd/gsql "CREATE UNDIRECTED EDGE TAGGED (FROM User, TO Movie, tag STRING, timestamp UINT)"
docker exec tigergraph //home/tigergraph/tigergraph/app/4.1.0/cmd/gsql "CREATE UNDIRECTED EDGE HAS_GENRE (FROM Movie, TO Genre)"
docker exec tigergraph //home/tigergraph/tigergraph/app/4.1.0/cmd/gsql "CREATE GRAPH movielens(User, Movie, Genre, RATED, TAGGED, HAS_GENRE)"
docker exec tigergraph //home/tigergraph/tigergraph/app/4.1.0/cmd/gsql "INSTALL DATASET"

# docker cp ../datasets/ml-32m/movies.csv tigergraph:/home/tigergraph/tigergraph/data/gsql/movies.csv
# docker cp ../datasets/ml-32m/tags.csv tigergraph:/home/tigergraph/tigergraph/data/gsql/tags.csv
# docker cp ../datasets/ml-32m/ratings.csv tigergraph:/home/tigergraph/tigergraph/data/gsql/ratings.csv
# docker cp ../datasets/ml-32m/genres.csv tigergraph:/home/tigergraph/tigergraph/data/gsql/genres.csv
# docker cp ../datasets/ml-32m/users.csv tigergraph:/home/tigergraph/tigergraph/data/gsql/users.csv

docker exec tigergraph //home/tigergraph/tigergraph/app/4.1.0/cmd/gsql "SHOW GRAPH movielens"
docker exec -it tigergraph //home/tigergraph/tigergraph/app/4.1.0/cmd/gadmin "restart gsql"

# Running algorithms
#docker exec -tigergraph sh
#//home/tigergraph/tigergraph/app/4.1.0/cmd//gsql SET query_timeout=60
# gsql
# USE GRAPH movielens
# RUN QUERY tg_betweenness_cent 
INSTALL QUERY tg_louvain
INSTALL QUERY tg_betweenness_cent
INTERPRET QUERY (/* Parameters here */) FOR GRAPH movielenssmall { 
  all = {ANY};

# Deleting everything
#DROP USERS
#DROP EDGES
#DROP GRAPH
#DROP ALL QUERIES
#DROP ALL JOBS
# CLEAR GRAPH STORE -HARD
INTERPRET QUERY () FOR GRAPH movielens { 
  all = {ANY};
  results = SELECT a FROM all:a - (:e) - ANY
  ACCUM
    DELETE(e)
  POST-ACCUM
    DELETE(a);
}

docker exec tigergraph gsql "USE GRAPH movielens
DROP VERTEX Movie;
CREATE VERTEX Movie (PRIMARY_ID id UINT, title STRING, genres STRING);"

docker exec -it  -u 0 tigergraph sh
apt-get update
apt-get install nano
nano ~/.bashrc
export PATH=$PATH:/home/tigergraph/tigergraph/app/4.1.0/cmd
. ~/.bashrc

gsql
use global CREATE GLOBAL SCHEMA_CHANGE JOB add_genres_to_movie {ALTER VERTEX Movie ADD ATTRIBUTE (gen
res STRING);}
RUN GLOBAL SCHEMA_CHANGE JOB add_genres_to_movie

use global CREATE GLOBAL SCHEMA_CHANGE JOB fix_genres {ALTER VERTEX Genre ADD ATTRIBUTE (name STRING);}
run global schema_change job fix_genres