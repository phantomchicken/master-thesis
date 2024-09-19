#!/bin/bash

# Check if the ml-10M100K folder exists, if not, download and unzip the dataset
if [ ! -d "ml-10M100K" ]; then
    echo "ml-10M100K folder not found. Downloading dataset..."
    wget https://files.grouplens.org/datasets/movielens/ml-10m.zip
    unzip ml-10m.zip
    echo "Dataset downloaded and unzipped."
else
    echo "ml-10M100K folder found."
fi

rm ml-10m.zip
# Change to the dataset directory
cd ml-10M100K

# Renaming the .dat files to .csv
mv "movies.dat" "movies.csv"
mv "ratings.dat" "ratings.csv"
mv "tags.dat" "tags.csv"
rm -f "genres.csv"
rm README.html
rm split_ratings.sh
rm allbut.pl


# Paths to your CSV files
MOVIES_CSV="movies.csv"
RATINGS_CSV="ratings.csv"
TAGS_CSV="tags.csv"
GENRES_CSV="genres.csv"
OUTPUT_CSV="movie_genre_edges.csv"

# Output files for preprocessed data
GENRES_OUTPUT="genres.csv"
USERS_OUTPUT="users.csv"

# Predefined genres
echo "genreId,name" > genres.csv
echo "1,Action" >> genres.csv
echo "2,Adventure" >> genres.csv
echo "3,Animation" >> genres.csv
echo "4,Children" >> genres.csv # Children not Children's (mistake in README)
echo "5,Comedy" >> genres.csv
echo "6,Crime" >> genres.csv
echo "7,Documentary" >> genres.csv
echo "8,Drama" >> genres.csv
echo "9,Fantasy" >> genres.csv
echo "10,Film-Noir" >> genres.csv
echo "11,Horror" >> genres.csv
echo "12,Musical" >> genres.csv
echo "13,Mystery" >> genres.csv
echo "14,Romance" >> genres.csv
echo "15,Sci-Fi" >> genres.csv
echo "16,Thriller" >> genres.csv
echo "17,War" >> genres.csv
echo "18,Western" >> genres.csv

# Extract unique users from ratings.csv and tags.csv
echo "Extracting users..."

if [ -f "$USERS_OUTPUT" ]; then
    echo "$USERS_OUTPUT already exists. Skipping user extraction."
else
    # Use awk to handle the '::' delimiter and extract the first field (user ID)
    awk -F"::" '{print $1}' $RATINGS_CSV > temp_users_ratings.csv
    awk -F"::" '{print $1}' $TAGS_CSV >> temp_users_ratings.csv

    # Sort and remove duplicates
    echo "userId" > $USERS_OUTPUT
    sort temp_users_ratings.csv | uniq >> $USERS_OUTPUT
    rm temp_users_ratings.csv
    echo "Unique users saved to $USERS_OUTPUT"
fi

# Prepare headers and delimiters for movies.csv, tags.csv, and ratings.csv
echo "Preparing headers and delimiters for movies.csv, tags.csv, and ratings.csv..."
sed -i 's/::/%/g' $MOVIES_CSV
sed -i 's/::/|/g' $TAGS_CSV
sed -i 's/::/|/g' $RATINGS_CSV

if ! head -n 1 movies.csv | grep -q "movieId%title%genres"; then
    sed -i '1imovieId%title%genres' movies.csv
fi

if ! head -n 1 tags.csv | grep -q "userId|movieId|tag|timestamp"; then
    sed -i '1iuserId|movieId|tag|timestamp' tags.csv
fi

if ! head -n 1 ratings.csv | grep -q "userId|movieId|rating|timestamp"; then
    sed -i '1iuserId|movieId|rating|timestamp' ratings.csv
fi
echo "Preprocessed headers and delimiters for movies.csv, tags.csv, and ratings.csv"

# Generate movie-genre edge mappings using Bash
echo "Generating movie-genre edge mappings..."
python ../generategenres.py