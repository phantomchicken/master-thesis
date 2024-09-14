// 1. Find Communities of Users Based on Commonly Rated Movies (Louvain)
// This query finds communities of users who have rated the same movies using the Louvain algorithm for community detection.

CALL algo.louvain.stream('User', 'RATED', {write: true, writeProperty: 'community'}) 
YIELD nodeId, community
RETURN algo.getNodeById(nodeId).id AS userId, community
ORDER BY community;
// Explanation:
// Louvain Algorithm is applied to detect communities of users who rate the same movies. Each user is assigned a community label based on their interactions with movies.
// This query returns the user ID and their corresponding community.


// 2. Find the Shortest Path Between Two Users Based on Shared Movies (Dijkstra)
// This query calculates the shortest path between two users who have rated the same movie using the Dijkstra algorithm.

MATCH (u1:User {id: '1'}), (u2:User {id: '2'})
CALL algo.shortestPath.stream(u1, u2, 'RATED', {direction: 'OUTGOING'})
YIELD nodeId, cost
RETURN algo.getNodeById(nodeId).id AS userId, cost;
// Explanation:
// Dijkstra's Algorithm is used to calculate the shortest path between two users (User 1 and User 2) based on shared movies they've rated.
// This query returns the path with the associated costs (if any), showing the connected users and the shortest connection via movies.


// 3. Find Most Influential Movies Based on Tag Frequency (PageRank)
// This query ranks movies based on how frequently they are tagged by users, using the PageRank algorithm.

CALL algo.pageRank.stream('Movie', 'TAGGED', {iterations: 20, dampingFactor: 0.85})
YIELD nodeId, score
RETURN algo.getNodeById(nodeId).title AS movieTitle, score
ORDER BY score DESC
LIMIT 10;
// Explanation:
// PageRank is applied to the TAGGED relationships between users and movies, helping to find the most influential or popular movies based on how frequently they are tagged.
// The result shows the top 10 movies ranked by their PageRank score.


// 4. Find Top Genres by Average Rating
// This query calculates the average rating for each genre by aggregating the ratings for all movies in that genre.

MATCH (u:User)-[r:RATED]->(m:Movie)-[:HAS_GENRE]->(g:Genre)
WITH g.name AS genre, AVG(r.rating) AS avgRating
RETURN genre, avgRating
ORDER BY avgRating DESC
LIMIT 5;

// Explanation:
// This query computes the average rating of each genre based on the ratings given by users to movies in that genre.
// The result returns the top 5 genres with the highest average ratings.

// 5. Identify Users Who Tend to Tag the Same Movies (Jaccard Similarity)
// This query identifies pairs of users who frequently tag the same movies, using the Jaccard Similarity.

MATCH (u1:User)-[:TAGGED]->(m:Movie)<-[:TAGGED]-(u2:User)
WHERE u1.userId <> u2.userId
WITH u1, u2, COUNT(m) AS commonTags
MATCH (u1)-[:TAGGED]->(m1:Movie)
WITH u1, u2, commonTags, COUNT(m1) AS totalTags1
MATCH (u2)-[:TAGGED]->(m2:Movie)
WITH u1, u2, commonTags, totalTags1, COUNT(m2) AS totalTags2
WITH u1, u2, commonTags, totalTags1, totalTags2,
     (commonTags * 1.0) / (totalTags1 + totalTags2 - commonTags) AS jaccard
RETURN u1.userId AS user1, u2.userId AS user2, jaccard
ORDER BY jaccard DESC
LIMIT 10;


// Explanation:
// This query calculates the Jaccard Similarity between two users based on how often they tag the same movies.
// The result lists the top 10 pairs of users who tend to tag the same movies, sorted by their Jaccard similarity score.
