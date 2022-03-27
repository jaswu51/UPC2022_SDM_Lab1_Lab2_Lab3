from neo4j import GraphDatabase
def evolve_conference_paper_reviews(driver):
    print('Evoloving conference paper reviews')

    driver.session().run("""
        LOAD CSV WITH HEADERS FROM 'file:///output/conference_reviews.csv' AS row FIELDTERMINATOR ';' 
        MATCH (p:Paper{key:row.key})
        UNWIND split(row.reviewer, '|') AS rev
        MATCH (a:Author {name: rev})
        MERGE (a)-[r:REVIEWS]->(p)
        SET r.decision = "accept"
        SET r.textual_description = row.textual_description
    """)


def load_evolve_journal_paper_reviews(driver):
    print('Loading journal paper reviewers')

    driver.session().run("""
        LOAD CSV WITH HEADERS FROM 'file:///output/journal_reviews.csv' AS row FIELDTERMINATOR ';' 
        MATCH (p:Paper{key:row.key})
        UNWIND split(row.reviewer, '|') AS rev
        MATCH (a:Author {name: rev})
        MERGE (a)-[r:REVIEWS]->(p)
        SET r.decision = "accept"
        SET r.textual_description = row.textual_description
    """)


def evolve_authors_affiliations(driver):
    print('Evolving Authors with their affiliations')

    driver.session().run("""
        LOAD CSV WITH HEADERS FROM 'file:///output/authors_affiliation.csv' AS row FIELDTERMINATOR ';' 
        MERGE (o:Organization{name:row.affiliation})
        with row, o
        MATCH (a:Author {name: row.author})
        MERGE (a)-[:IS_AFFILIATED_TO]->(o)
    """)


def evolve_add_years(driver):
    print("Evolve the years in journal and journal title")
    driver.session.run('''
        MATCH (p:Paper)<--(v:Volomn)
        MERGE
    ''')


uri, user, password = "bolt://localhost:7687", "neo4j", "password"
driver = GraphDatabase.driver(uri, auth=(user, password))
evolve_conference_paper_reviews(driver)
load_evolve_journal_paper_reviews(driver)
evolve_authors_affiliations(driver)
driver.close()