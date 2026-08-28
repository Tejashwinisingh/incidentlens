// 1. Parameterised incident lookup
MATCH (i:Incident {id:$incidentId})
RETURN i;

// 2. Required multi-hop traversal (Incident -> Service -> Application)
MATCH (i:Incident {id:$incidentId})-[:AFFECTS]->(s:Service)-[:USES]->(a:Application)
RETURN i,s,a;

// 3. Graph-specific related incidents through a shared service
MATCH (i:Incident {id:$incidentId})-[:AFFECTS]->(s:Service)<-[:AFFECTS]-(related:Incident)
WHERE related.id <> $incidentId
RETURN DISTINCT related;

// 4. Multi-hop infrastructure path
MATCH (i:Incident {id:$incidentId})-[:AFFECTS]->(s:Service)-[:USES]->(a:Application)
      -[:RUNS_ON]->(srv:Server)-[:CONTAINS]->(c:Component)
RETURN s,a,srv,c;
