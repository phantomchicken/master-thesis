CREATE INDEX ON :Gene(name);

MATCH (g1:Gene {name: "SERPINF2"})-[*..2]-(g2:Gene {name: "BRCA1"})
RETURN g1, g2;

MATCH (g:Gene {name: "SERPINF2"})-[:PARTICIPATES_GpPW]-(p:Pathway)
RETURN p.name, p.id;

Caffeine
VEGFC melanoma cancer

    Find Diseases That Share Symptoms with "Crohn's Disease"
    MATCH (d1:Disease {name: "lung cancer"})-[:PRESENTS_DpS]-(s:Symptom)<-[:PRESENTS_DpS]-(d2:Disease)
    RETURN d2.name, s.name;


    Find all genes associated with both liver and kidney cancer
    MATCH (source:Disease)-[:ASSOCIATES_DaG]-(gene:Gene)-[:ASSOCIATES_DaG]-(target:Disease)
    WHERE source.name = 'liver cancer'
    AND target.name = 'kidney cancer'
    RETURN
    gene.name AS gene_symbol,
    gene.description AS gene_name,
    gene.url AS url
    ORDER BY gene_symbol

    3. Find All Genes Linked to a Disease via Multiple Relationships
    MATCH (d:Disease {name: "azoospermia"})-[:DOWNREGULATES_DdG|:UPREGULATES_DuG|:ASSOCIATES_DaG]-(g:Gene)
    RETURN g.name, count(*) AS num_associations
    ORDER BY num_associations DESC
    LIMIT 10

    5. Find All Diseases that Share Similar Symptoms Using Multi-Hop Query
    cypher
    Copy code
    MATCH (d1:Disease)-[:PRESENTS_DpS]->(s:Symptom)<-[:PRESENTS_DpS]-(d2:Disease)
    RETURN DISTINCT d1.name, d2.name, count(s) AS shared_symptoms
    ORDER BY shared_symptoms DESC
    LIMIT 10
    Benchmark Goal: Find diseases that share common symptoms. This query uses a multi-hop relationship with an aggregate function.
    
    7SEK7. Find the Top 5 Most Connected Genes (By Relationships)
    MATCH (g:Gene)
    OPTIONAL MATCH (g)--()
    RETURN g.name, COUNT(*) AS degree
    ORDER BY degree DESC
    LIMIT 5;
    
    10SEKFind All Pathways Shared by Multiple Genes
    MATCH (g1:Gene)-[:PARTICIPATES_GpPW]->(p:Pathway)<-[:PARTICIPATES_GpPW]-(g2:Gene)
    RETURN p.name, count(DISTINCT g1) AS num_genes
    ORDER BY num_genes DESC
    LIMIT 10

    1.5SEKFind the Shortest Path Between Two Genes via Shared Diseases
    MATCH p=(g1:Gene {name: "SERPINF2"})-[:ASSOCIATES_DaG*BFS]-(g2:Gene {name: "BRCA1"})
    RETURN p;

    2SEK Finding Diseases/Conditions Linked to Asthma and Coughing:
    MATCH path=(d1:Disease {name: "asthma"})-[:PRESENTS_DpS|ASSOCIATES_DaG|TREATS_CtD*BFS]-(d:Disease)-[:PRESENTS_DpS|ASSOCIATES_DaG|TREATS_CtD*BFS]-(s1:Symptom {name: "Cough"})
    RETURN DISTINCT d.name AS Disease, d1.name AS Related_To_Asthma, s1.name AS Related_To_Cough, path
    ORDER BY d.name;


    MATCH path = (n0:Disease)-[e1:ASSOCIATES_DaG]-(n1)-[:INTERACTS_GiG]-(n2)-[:PARTICIPATES_GpBP]-(n3:BiologicalProcess)
    WHERE n0.name = 'multiple sclerosis'
    AND n3.name = 'retina layer formation'
    AND 'GWAS Catalog' in e1.sources
    AND exists((n0)-[:LOCALIZES_DlA]-()-[:UPREGULATES_AuG]-(n2))
    RETURN path