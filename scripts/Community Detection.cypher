CALL gds.graph.project('graph', 'Person', 'SOCIAL_RELATIONSHIP')
CALL gds.degree.stream('graph')
    YIELD nodeId, score
    RETURN gds.util.asNode(nodeId).name AS title, score AS connections
    ORDER BY score DESCENDING, title LIMIT 15