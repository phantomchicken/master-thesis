// Q1: Find all the movies in a specific genre (e.g., Action): 300ms
MATCH (m:Movie)-[:HAS_GENRE]->(g:Genre {name: "Action"}) 
RETURN m.title;

// Q2: Find the top 5 highest-rated movies (average rating)  30s
MATCH (m:Movie)<-[r:RATED]-(u:User)
RETURN m.title, AVG(r.rating) AS avg_rating
ORDER BY avg_rating DESC
LIMIT 5;

// Q3: List the genres with the most movies 183ms
MATCH (m:Movie)-[:HAS_GENRE]->(g:Genre)
RETURN g.name, COUNT(m) AS movie_count
ORDER BY movie_count DESC;

// Q4: Find users who rated a specific movie (e.g., "Toy Story"):2,5s
MATCH (u:User)-[r:RATED]->(m:Movie {title: "Toy Story (1995)"})
RETURN u.userId, r.rating;

// Q5: Find the top 5 movies with the most distinct users who rated them 10S
MATCH (u:User)-[:RATED]->(m:Movie)
RETURN m.title, COUNT(DISTINCT u.userId) AS num_users
ORDER BY num_users DESC
LIMIT 5;

// Q6: Find the user with the most ratings 14s
MATCH (u:User)-[r:RATED]->(m:Movie)
RETURN u.userId, COUNT(r) AS total_ratings
ORDER BY total_ratings DESC
LIMIT 1;

// Q7: Find the st. deviation for a movie (e.g., "Forrest Gump") 10S
MATCH (m:Movie {title: "Forrest Gump (1994)"})<-[r:RATED]-(u:User) 
RETURN STDEV(r.rating) AS ratingVariance;

// Mandatory for Q8-Q10
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

// Q8: Calculate PageRank for all nodes in the graph 180ms
CALL gds.pageRank.stream('movieGraph') 
YIELD nodeId, score
MATCH (m:Movie) WHERE id(m) = nodeId
RETURN m.title AS movie, score
ORDER BY score DESC
LIMIT 10;

// Q9: Calculate the betweenness centrality for all nodes in the graph 30s
CALL gds.betweenness.stream('m1') 
YIELD nodeId, score
MATCH (n) WHERE id(n) = nodeId
RETURN 
  CASE 
    WHEN labels(n)[0] = 'Movie' THEN n.title
    WHEN labels(n)[0] = 'User' THEN n.userId
    WHEN labels(n)[0] = 'Genre' THEN n.name
  END AS name_or_id, score
ORDER BY score DESC
LIMIT 10;

// Q10: Detect communities in the graph
CALL gds.louvain.stream('movieGraph')
YIELD nodeId, communityId
WITH nodeId, communityId
MATCH (n) WHERE id(n) = nodeId
WITH 
  CASE 
    WHEN labels(n)[0] = 'Movie' THEN n.title
    WHEN labels(n)[0] = 'User' THEN n.userId
    WHEN labels(n)[0] = 'Genre' THEN n.name
  END AS name_or_id, communityId
ORDER BY communityId
WITH communityId, COLLECT(name_or_id)[0..5] AS sample_per_community
UNWIND sample_per_community AS name_or_id
RETURN name_or_id, communityId
ORDER BY communityId;

/////////////////////////////////////////
CALL gds.pageRank.stream('m1', {
  maxIterations: 20,
  dampingFactor: 0.85
})
YIELD nodeId, score
MATCH (n) WHERE id(n) = nodeId
RETURN 
  CASE 
    WHEN labels(n)[0] = 'Movie' THEN n.title
    WHEN labels(n)[0] = 'User' THEN n.userId
    WHEN labels(n)[0] = 'Genre' THEN n.name
  END AS name_or_id, score
ORDER BY score DESC
LIMIT 100;
///////////////////////////////////////////
CREATE INDEX IF NOT EXISTS FOR (m:Movie) ON (m.movieId);
CREATE INDEX IF NOT EXISTS FOR (m:Movie) ON (m.title);
CREATE INDEX IF NOT EXISTS FOR (g:Genre) ON (g.name);
CREATE INDEX IF NOT EXISTS FOR (u:User) ON (u.userId);




CALL gds.graph.project(
  'm1',
  ['User', 'Movie','Genre'],
  {
    RATED: {
      type: 'RATED',
      properties: 'rating'
    },
     TAGGED: {
      type: 'TAGGED'
    },
    HAS_GENRE: {
      type: 'HAS_GENRE'
    }
  }
);

CALL gds.graph.project(
  'dijkstra',
  ['User', 'Movie','Genre'],
  {
    RATED: {
      type: 'RATED',
      properties: 'rating'
    }
  }
);

CALL gds.graph.project(
  'users',
  ['User'],
  {
    RATED: {
      type: 'RATED',
      properties: 'rating'
    },
     TAGGED: {
      type: 'TAGGED'
    }
  }
);

CALL gds.louvain.stream('m1')
YIELD nodeId, communityId
MATCH (n) WHERE id(n) = nodeId
RETURN 
  CASE 
    WHEN labels(n)[0] = 'Movie' THEN n.title
    WHEN labels(n)[0] = 'User' THEN n.userId
    WHEN labels(n)[0] = 'Genre' THEN n.name
  END AS name_or_id, communityId
ORDER BY communityId
LIMIT 100;

MATCH (m1:Movie {movieId: "1"})<-[:RATED]-(u:User)-[:RATED]->(m2:Movie {movieId: "6"})
RETURN m1.title, m2.title, u.userId;

MATCH (source:User {userId: "1"}), (target:User {userId: "1000"})
CALL gds.bfs.stream('dijkstra', {
  sourceNode: source,
  targetNodes: target
})
YIELD path
RETURN path, 
  [node IN nodes(path) | coalesce(node.userId, node.title)] AS pathDetails;



