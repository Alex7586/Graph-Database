// Nodes
LOAD CSV WITH HEADERS FROM 'file:///authors.csv' AS r
MERGE (:Author {id: r.id, name: r.name});

LOAD CSV WITH HEADERS FROM 'file:///papers.csv' AS r
MERGE (:Paper {id: r.id, title: r.title, year: toInteger(r.year)});

LOAD CSV WITH HEADERS FROM 'file:///venues.csv' AS r
MERGE (:Venue {id: r.id, name: r.name, type: r.type});

LOAD CSV WITH HEADERS FROM 'file:///institutions.csv' AS r
MERGE (:Institution {id: r.id, name: r.name, country: r.country});

LOAD CSV WITH HEADERS FROM 'file:///keywords.csv' AS r
MERGE (:Keyword {id: r.id, value: r.value});

// Relationships
LOAD CSV WITH HEADERS FROM 'file:///authored.csv' AS r
MATCH (a:Author {id: r.author_id})
MATCH (p:Paper  {id: r.paper_id})
MERGE (a)-[:AUTHORED {pos: toInteger(r.pos)}]->(p);

LOAD CSV WITH HEADERS FROM 'file:///cites.csv' AS r
MATCH (p1:Paper {id: r.src_paper_id})
MATCH (p2:Paper {id: r.dst_paper_id})
MERGE (p1)-[:CITES]->(p2);

LOAD CSV WITH HEADERS FROM 'file:///published_in.csv' AS r
MATCH (p:Paper {id: r.paper_id})
MATCH (v:Venue {id: r.venue_id})
MERGE (p)-[:PUBLISHED_IN]->(v);

LOAD CSV WITH HEADERS FROM 'file:///affiliated.csv' AS r
MATCH (a:Author {id: r.author_id})
MATCH (i:Institution {id: r.inst_id})
MERGE (a)-[:AFFILIATED_WITH {since: toInteger(r.since)}]->(i);

LOAD CSV WITH HEADERS FROM 'file:///has_keyword.csv' AS r
MATCH (p:Paper {id: r.paper_id})
MATCH (k:Keyword {id: r.keyword_id})
MERGE (p)-[:HAS_KEYWORD]->(k);
