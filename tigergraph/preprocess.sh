#!/bin/bash

# Paths to your CSV files
MOVIES_CSV="../datasets/ml-32m/movies.csv"
RATINGS_CSV="../datasets/ml-32m/ratings.csv"
TAGS_CSV="../datasets/ml-32m/tags.csv"

# Output files for preprocessed data
GENRES_OUTPUT="../datasets/ml-32m/genres.csv"
USERS_OUTPUT="../datasets/ml-32m/users.csv"

echo "Extracting genres..."

# Using awk to handle commas inside quotes properly
awk -F ',' 'BEGIN {OFS=","} {
    # Find where the genres are (last column)
    gsub(/\"/, "", $0); 
    split($0, arr, ","); 
    genres = arr[length(arr)]; 
    gsub(/\|/, "\n", genres); 
    print genres
}' $MOVIES_CSV | sort | uniq > $GENRES_OUTPUT

echo "Unique genres saved to $GENRES_OUTPUT"

# Extract unique users from ratings.csv and tags.csv
echo "Extracting users..."
cut -d',' -f1 $RATINGS_CSV > temp_users_ratings.csv
cut -d',' -f1 $TAGS_CSV >> temp_users_ratings.csv

# Sort and remove duplicates
sort temp_users_ratings.csv | uniq > $USERS_OUTPUT
rm temp_users_ratings.csv

echo "Unique users saved to $USERS_OUTPUT"
