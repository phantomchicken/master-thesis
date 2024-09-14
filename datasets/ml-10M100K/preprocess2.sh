#!/bin/bash

# Renaming the .dat files to .csv
mv "movies.dat" "movies.csv"
mv "ratings.dat" "ratings.csv"
mv "tags.dat" "tags.csv"
rm "genres.csv"

# Paths to your CSV files
MOVIES_CSV="movies.csv"
RATINGS_CSV="ratings.csv"
TAGS_CSV="tags.csv"

# Output files for preprocessed data
GENRES_OUTPUT="genres.csv"
USERS_OUTPUT="users.csv"

# Predefined genres
echo "Action" > genres.csv
echo "Adventure" >> genres.csv
echo "Animation" >> genres.csv
echo "Children's" >> genres.csv
echo "Comedy" >> genres.csv
echo "Crime" >> genres.csv
echo "Documentary" >> genres.csv
echo "Drama" >> genres.csv
echo "Fantasy" >> genres.csv
echo "Film-Noir" >> genres.csv
echo "Horror" >> genres.csv
echo "Musical" >> genres.csv
echo "Mystery" >> genres.csv
echo "Romance" >> genres.csv
echo "Sci-Fi" >> genres.csv
echo "Thriller" >> genres.csv
echo "War" >> genres.csv
echo "Western" >> genres.csv

# Extract unique users from ratings.csv and tags.csv
echo "Extracting users..."

# Use awk to handle the '::' delimiter and extract the first field (user ID)
awk -F"::" '{print $1}' $RATINGS_CSV > temp_users_ratings.csv
awk -F"::" '{print $1}' $TAGS_CSV >> temp_users_ratings.csv

# Sort and remove duplicates
sort temp_users_ratings.csv | uniq > $USERS_OUTPUT
rm temp_users_ratings.csv

echo "Unique users saved to $USERS_OUTPUT"

#change movies delimiter to %
#change tags delimiter to | 
#change ratings delimiter to |