import csv

# Split genres from movies.csv and create a mapping of genre name to genre ID

# Paths to files
movies_csv = '../datasets/ml-10M100K/movies.csv'
genres_csv = '../datasets/ml-10M100K/genrestiger.csv'
output_csv = '../datasets/ml-10M100K/movie_genre_edges.csv'

# Read genres and create a mapping of genre name to genre ID
genre_mapping = {}
with open(genres_csv, 'r', encoding='utf-8') as f_genres:
    reader = csv.reader(f_genres, delimiter='|')
    for row in reader:
        genre_mapping[row[1]] = row[0]  # Map genre name to genre ID

# Process movies.csv and generate movie-genre edge mappings
with open(movies_csv, 'r', encoding='utf-8') as f_movies, open(output_csv, 'w', newline='') as f_output:
    reader = csv.reader(f_movies, delimiter='%')
    writer = csv.writer(f_output)
    
    # Write header for the output file
    writer.writerow(['movieId', 'genreId'])
    
    # Process each movie and create edges
    next(reader)  # Skip header in movies.csv
    for row in reader:
        movie_id = row[0]
        genres = row[2].split('|')  # Split genres by '|'
        
        for genre in genres:
            genre = genre.strip()
            if genre in genre_mapping:
                genre_id = genre_mapping[genre]
                writer.writerow([movie_id, genre_id])

print(f"Edges file {output_csv} generated successfully!")
