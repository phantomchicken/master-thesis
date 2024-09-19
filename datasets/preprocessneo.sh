#!/bin/bash

# Folder for Neo4j import
NEO4J_DIR="./ml-10M100K/neo4j-import"
SOURCE_DIR="./ml-10M100K"
FILES=("movies.csv" "users.csv" "genres.csv" "tags.csv" "movie_genre_edges.csv" "ratings.csv")

# Create the Neo4j import folder
mkdir -p $NEO4J_DIR

# 1. Movies Nodes (retain '|' in genres field, use '%' delimiter everywhere else)
echo "Processing movies.csv..."
cp "$SOURCE_DIR/movies.csv" "$NEO4J_DIR/movies.csv"
sed -i '1s/.*/movieId:ID(Movie-ID)%title%genres/' "$NEO4J_DIR/movies.csv"
sed -i 's/\"//g' "$NEO4J_DIR/movies.csv" # Remove double quotes
sed -i 's/,/%/g' "$NEO4J_DIR/movies.csv"

# 2. Users Nodes
echo "Processing users.csv..."
cp "$SOURCE_DIR/users.csv" "$NEO4J_DIR/users.csv"
sed -i '1s/.*/userId:ID(User-ID)/' "$NEO4J_DIR/users.csv"
sed -i 's/\"//g' "$NEO4J_DIR/users.csv"

# 3. Genres Nodes
echo "Processing genres.csv..."
cp "$SOURCE_DIR/genres.csv" "$NEO4J_DIR/genres.csv"
sed -i '1s/.*/genreId:ID(Genre-ID)%name/' "$NEO4J_DIR/genres.csv"
sed -i 's/\"//g' "$NEO4J_DIR/genres.csv"

# 4. Tags Relationships (user - TAGGED - movie)
echo "Processing tags.csv..."
cp "$SOURCE_DIR/tags.csv" "$NEO4J_DIR/tags.csv"
sed -i '1s/.*/:START_ID(User-ID)%:END_ID(Movie-ID)%tag%timestamp%:TYPE/' "$NEO4J_DIR/tags.csv"
sed -i 's/\"//g' "$NEO4J_DIR/tags.csv" # Remove double quotes

# 5. Movie-Genre Relationships (movie - HAS_GENRE - genre)
echo "Processing movie_genre_edges.csv..."
cp "$SOURCE_DIR/movie_genre_edges.csv" "$NEO4J_DIR/movie_genre_edges.csv"
sed -i '1s/.*/:START_ID(Movie-ID)%:END_ID(Genre-ID)%:TYPE/' "$NEO4J_DIR/movie_genre_edges.csv"
# Replace the relationship type with HAS_GENRE
sed -i 's/$/%HAS_GENRE/' "$NEO4J_DIR/movie_genre_edges.csv"

# 6. Ratings Relationships (user - RATED - movie)
echo "Processing ratings.csv..."
cp "$SOURCE_DIR/ratings.csv" "$NEO4J_DIR/ratings.csv"
sed -i '1s/.*/:START_ID(User-ID)%:END_ID(Movie-ID)%rating%timestamp%:TYPE/' "$NEO4J_DIR/ratings.csv"
# Replace the relationship type with RATED
sed -i 's/$/%RATED/' "$NEO4J_DIR/ratings.csv"

# Process all ratings files from ratings00 to ratings10
for i in {00..10}; do
  echo "Processing ratings${i}.csv..."
  cp "$SOURCE_DIR/ratings${i}.csv" "$NEO4J_DIR/ratings${i}.csv"
  sed -i '1s/.*/:START_ID(User-ID)%:END_ID(Movie-ID)%rating%timestamp%:TYPE/' "$NEO4J_DIR/ratings${i}.csv"
  sed -i 's/$/%RATED/' "$NEO4J_DIR/ratings${i}.csv"
done

echo "All files have been processed and copied to the $NEO4J_DIR directory."

# Copy the files into the Neo4j container for import
CONTAINER_NAME="neo4j" # Replace with your Neo4j container name
docker cp $NEO4J_DIR/movies.csv "$CONTAINER_NAME":/var/lib/neo4j/import/movies.csv
docker cp $NEO4J_DIR/ratings.csv "$CONTAINER_NAME":/var/lib/neo4j/import/ratings.csv
docker cp $NEO4J_DIR/tags.csv "$CONTAINER_NAME":/var/lib/neo4j/import/tags.csv
docker cp $NEO4J_DIR/genres.csv "$CONTAINER_NAME":/var/lib/neo4j/import/genres.csv
docker cp $NEO4J_DIR/users.csv "$CONTAINER_NAME":/var/lib/neo4j/import/users.csv
docker cp $NEO4J_DIR/movie_genre_edges.csv "$CONTAINER_NAME":/var/lib/neo4j/import/movie_genre_edges.csv
docker cp $NEO4J_DIR/ratings{00..10}.csv "$CONTAINER_NAME":/var/lib/neo4j/import/
