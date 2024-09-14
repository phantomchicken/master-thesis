Find all the movies in a specific genre (e.g., Action): 300ms
MATCH (m:Movie)-[:HAS_GENRE]->(g:Genre {name: "Action"}) 
RETURN m.title;

Find the top 5 highest-rated movies (average rating): 30s
MATCH (m:Movie)<-[r:RATED]-(u:User)
RETURN m.title, AVG(r.rating) AS avg_rating
ORDER BY avg_rating DESC
LIMIT 5;

List the genres with the most movies: 183ms
MATCH (m:Movie)-[:HAS_GENRE]->(g:Genre)
RETURN g.name, COUNT(m) AS movie_count
ORDER BY movie_count DESC;

Find users who rated a specific movie (e.g., "Toy Story"): 2,5s
MATCH (u:User)-[r:RATED]->(m:Movie {title: "Toy Story (1995)"})
RETURN u.userId, r.rating;

Find the top 5 movies with the highest number of distinct users who rated them: 10S
MATCH (u:User)-[:RATED]->(m:Movie)
RETURN m.title, COUNT(DISTINCT u.userId) AS num_users
ORDER BY num_users DESC
LIMIT 5;

Most ratings 14s
MATCH (u:User)-[r:RATED]->(m:Movie)
RETURN u.userId, COUNT(r) AS total_ratings
ORDER BY total_ratings DESC
LIMIT 1;
