import csv
import os

# Split genres from movies.csv and create a mapping of genre name to genre ID
base_dir = os.path.join(os.getcwd(), 'ml-10M100K')
movies_csv = os.path.join(base_dir, 'movies.csv')
genres_csv = os.path.join(base_dir, 'genres.csv')
output_csv = os.path.join(base_dir, 'movie_genre_edges.csv')

# Check if the necessary files exist
if not os.path.exists(movies_csv):
    print(f"Error: {movies_csv} not found.")
    exit(1)

if not os.path.exists(genres_csv):
    print(f"Error: {genres_csv} not found.")
    exit(1)

if os.path.exists(output_csv):
    print(f"{output_csv} already exists. Skipping generation.")
    exit(0)

# Read genres and create a mapping of genre name to genre ID
genre_mapping = {}
with open(genres_csv, 'r', encoding='utf-8', newline='') as f_genres:
    reader = csv.DictReader(f_genres, delimiter=',')
    for row in reader:
        genre_mapping[row['name']] = row['genreId']  # Map genre name to genre ID

# Buffer to store rows before writing to the file in bulk
batch_size = 1000
buffer = []

# Process movies.csv and generate movie-genre edge mappings
with open(movies_csv, 'r', encoding='utf-8', newline='') as f_movies, open(output_csv, 'w', newline='', buffering=1000000) as f_output:
    reader = csv.DictReader(f_movies, delimiter='%')
    writer = csv.writer(f_output)
    
    # Write header for the output file
    writer.writerow(['movieId', 'genreId'])
    
    # Process each movie and create edges
    for row in reader:
        movie_id = row['movieId']
        genres = row['genres'].split('|')  # Split genres by '|'
        
        for genre in genres:
            genre = genre.strip()  # Trim spaces
            genre_id = genre_mapping.get(genre)
            if genre_id:
                buffer.append([movie_id, genre_id])
        
        # Write in batches to improve performance
        if len(buffer) >= batch_size:
            writer.writerows(buffer)
            buffer.clear()

    # Write remaining rows in the buffer
    if buffer:
        writer.writerows(buffer)

print(f"Edges file {output_csv} generated successfully!")
