// Q1: Find all the movies in a specific genre (e.g., Action): 18ms
MATCH (m:Movie)-[:HAS_GENRE]->(g:Genre {name: "Action"}) 
RETURN m.title;

// Q2: Find the top 5 highest-rated movies (average rating) 6s
MATCH (m:Movie)<-[r:RATED]-(u:User)
RETURN m.title, AVG(r.rating) AS avg_rating
ORDER BY avg_rating DESC
LIMIT 5;

// Q3: List the genres with the most movies 20ms
MATCH (m:Movie)-[:HAS_GENRE]->(g:Genre)
RETURN g.name, COUNT(m) AS movie_count
ORDER BY movie_count DESC;

// Q4: Find users who rated a specific movie (e.g., "Toy Story"): 323ms
MATCH (u:User)-[r:RATED]->(m:Movie {title: "Toy Story (1995)"})
RETURN u.userId, r.rating;

// u.userId = u.id in memgraph!!!
// Q5: Find the top 5 movies with the most distinct users who rated them 7S
MATCH (u:User)-[:RATED]->(m:Movie)
RETURN m.title, COUNT(DISTINCT u.userId) AS num_users
ORDER BY num_users DESC
LIMIT 5;

// u.userId = u.id in memgraph!!! 2,61s
// Q6: Find the user with the most ratings
MATCH (u:User)-[r:RATED]->(m:Movie)
RETURN u.userId, COUNT(r) AS total_ratings
ORDER BY total_ratings DESC
LIMIT 1;

// no stdev! 3S
// Q7: Find the st. deviation for a movie (e.g., "Forrest Gump")
MATCH (m:Movie {title: "Forrest Gump (1994)"})<-[r:RATED]-(u:User)
WITH avg(r.rating) AS avgRating, collect(r.rating) AS ratings
WITH avgRating, ratings, size(ratings) AS count
UNWIND ratings AS rating
RETURN sqrt(sum((rating - avgRating) * (rating - avgRating)) / count) AS ratingVariance;

// Q8: Calculate PageRank for all nodes in the graph
CALL pagerank.get(20, 0.85, 1e-05)
YIELD node, rank
RETURN node, rank
ORDER BY rank DESC
LIMIT 10;

// 47s really small values
// Q9: Calculate the betweenness centrality for all nodes in the graph
CALL betweenness_centrality.get(True, True) 
YIELD node, betweenness_centrality
RETURN node, betweenness_centrality
ORDER BY betweenness_centrality DESC
LIMIT 10;

// 57s
// Q10: Detect communities in the graph
CALL community_detection.get()
YIELD node, community_id;

///////////////////////////////////////////
CREATE INDEX IF NOT EXISTS FOR (m:Movie) ON (m.movieId);
CREATE INDEX IF NOT EXISTS FOR (m:Movie) ON (m.title);
CREATE INDEX IF NOT EXISTS FOR (g:Genre) ON (g.name);
CREATE INDEX IF NOT EXISTS FOR (u:User) ON (u.userId);

CALL gds.graph.project(
  'movieGraph',
  'Movie',
  {
    RATED: {
      type: 'RATED',
      properties: 'rating'
    }
  }
);