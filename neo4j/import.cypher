:param BASE_URL => "https://raw.githubusercontent.com/Alex7586/Graph-Database/main/data";

// Nodes
LOAD CSV WITH HEADERS FROM ($BASE_URL + '/authors.csv') AS r
MERGE (:Author {id: r.id, name: r.name});

LOAD CSV WITH HEADERS FROM ($BASE_URL + '/papers.csv') AS r
MERGE (:Paper {id: r.id, title: r.title, year: toInteger(r.year)});

LOAD CSV WITH HEADERS FROM ($BASE_URL + '/venues.csv') AS r
MERGE (:Venue {id: r.id, name: r.name, type: r.type});

LOAD CSV WITH HEADERS FROM ($BASE_URL + '/institutions.csv') AS r
MERGE (:Institution {id: r.id, name: r.name, country: r.country});

LOAD CSV WITH HEADERS FROM ($BASE_URL + '/keywords.csv') AS r
MERGE (:Keyword {id: r.id, value: r.value});

// Relationships
LOAD CSV WITH HEADERS FROM ($BASE_URL + '/authored.csv') AS r
MATCH (a:Author {id: r.author_id})
MATCH (p:Paper  {id: r.paper_id})
MERGE (a)-[:AUTHORED {pos: toInteger(r.pos)}]->(p);

LOAD CSV WITH HEADERS FROM ($BASE_URL + '/cites.csv') AS r
MATCH (p1:Paper {id: r.src_paper_id})
MATCH (p2:Paper {id: r.dst_paper_id})
MERGE (p1)-[:CITES]->(p2);

LOAD CSV WITH HEADERS FROM ($BASE_URL + '/published_in.csv') AS r
MATCH (p:Paper {id: r.paper_id})
MATCH (v:Venue {id: r.venue_id})
MERGE (p)-[:PUBLISHED_IN]->(v);

LOAD CSV WITH HEADERS FROM ($BASE_URL + '/affiliated.csv') AS r
MATCH (a:Author {id: r.author_id})
MATCH (i:Institution {id: r.inst_id})
MERGE (a)-[:AFFILIATED_WITH {since: toInteger(r.since)}]->(i);

LOAD CSV WITH HEADERS FROM ($BASE_URL + '/has_keyword.csv') AS r
MATCH (p:Paper {id: r.paper_id})
MATCH (k:Keyword {id: r.keyword_id})
MERGE (p)-[:HAS_KEYWORD]->(k);

MATCH (a1:Author)-[:AUTHORED]->(p:Paper)<-[:AUTHORED]-(a2:Author)
WHERE a1.id < a2.id
MERGE (a1)-[:COAUTHOR]->(a2)
MERGE (a2)-[:COAUTHOR]->(a1);

