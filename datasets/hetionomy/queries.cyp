1. Find the Shortest Path Between Two Genes via Shared Diseases
cypher
Copy code
MATCH p=shortestPath((g1:Gene {name: "SERPINF2"})-[:ASSOCIATES_DaG*]-(g2:Gene {name: "BRCA1"}))
RETURN p
Benchmark Goal: Pathfinding between two genes through diseases they are both associated with. This involves multi-hop traversals across the graph.

2. Find All Diseases Connected to a Specific Gene Through Pathways (Up to 3 Hops)
cypher
Copy code
MATCH (g:Gene {name: "SERPINF2"})-[:PARTICIPATES_GpPW|PARTICIPATES_GpBP*1..3]-(d:Disease)
RETURN DISTINCT d.name
Benchmark Goal: A multi-hop query (1 to 3 hops) that looks for diseases connected to a gene via Pathways and Biological Processes.

3. Find All Genes Linked to a Disease via Multiple Relationships
cypher
Copy code
MATCH (d:Disease {name: "azoospermia"})-[:DOWNREGULATES_DdG|:UPREGULATES_DuG|:ASSOCIATES_DaG]-(g:Gene)
RETURN g.name, count(*) AS num_associations
ORDER BY num_associations DESC
LIMIT 10
Benchmark Goal: Complex querying using multiple relationships (DOWNREGULATES_DdG, UPREGULATES_DuG, ASSOCIATES_DaG), aggregation, and ordering based on the number of associations.

4. Find the All Genes That Participate in Pathways Involving Molecular Functions
cypher
Copy code
MATCH (g:Gene)-[:PARTICIPATES_GpPW]->(p:Pathway)-[:PARTICIPATES_GpMF]->(mf:MolecularFunction)
RETURN g.name, p.name, mf.name
LIMIT 20
Benchmark Goal: Multi-hop query traversing from Genes to Pathways and Molecular Functions. This query tests the ability to chain multiple relationships.

5. Find All Diseases that Share Similar Symptoms Using Multi-Hop Query
cypher
Copy code
MATCH (d1:Disease)-[:PRESENTS_DpS]->(s:Symptom)<-[:PRESENTS_DpS]-(d2:Disease)
RETURN DISTINCT d1.name, d2.name, count(s) AS shared_symptoms
ORDER BY shared_symptoms DESC
LIMIT 10
Benchmark Goal: Find diseases that share common symptoms. This query uses a multi-hop relationship with an aggregate function.

6. Identify All Compounds That Affect Gene Expression (Direct or Indirect)
cypher
Copy code
MATCH (c:Compound)-[:UPREGULATES_CuG|:DOWNREGULATES_CdG*1..3]-(g:Gene)
RETURN c.name, g.name
LIMIT 20
Benchmark Goal: Multi-hop traversal up to 3 hops between Compounds and Genes via gene expression relationships (UPREGULATES_CuG and DOWNREGULATES_CdG).

7. Find the Top 5 Most Connected Genes (By Relationships)
cypher
Copy code
MATCH (g:Gene)
RETURN g.name, size((g)--()) AS degree
ORDER BY degree DESC
LIMIT 5
Benchmark Goal: This query calculates the degree (number of connections) of each gene and returns the top 5 most connected genes.

8. Find All Pathways Shared by Multiple Genes
cypher
Copy code
MATCH (g1:Gene)-[:PARTICIPATES_GpPW]->(p:Pathway)<-[:PARTICIPATES_GpPW]-(g2:Gene)
RETURN p.name, count(DISTINCT g1) AS num_genes
ORDER BY num_genes DESC
LIMIT 10
Benchmark Goal: This query finds the pathways that are shared by the most genes, using aggregation and multi-hop traversal.

9. Find All Diseases Treated by Compounds That Also Cause Side Effects
cypher
Copy code
MATCH (c:Compound)-[:TREATS_CtD]->(d:Disease), (c)-[:CAUSES_CcSE]->(se:Sideeffect)
RETURN d.name, se.name, c.name
LIMIT 20
Benchmark Goal: Complex query that checks both the TREATS_CtD and CAUSES_CcSE relationships for a compound, and returns diseases and side effects connected to that compound.

10. Find the Longest Path Between Two Diseases (Via Compounds, Genes, and Symptoms)
cypher
Copy code
MATCH p=allShortestPaths((d1:Disease)-[:TREATS_CtD|ASSOCIATES_DaG|PRESENTS_DpS*1..5]-(d2:Disease))
RETURN p
ORDER BY length(p) DESC
LIMIT 1
Benchmark Goal: A longer traversal path across diseases, compounds, genes, and symptoms using multi-hop traversal with a variety of relationships.