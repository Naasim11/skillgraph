import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

class Database:
    def __init__(self):
        self.uri = os.getenv("COGNODB_URI")
        self.username = os.getenv("COGNODB_USERNAME")
        self.password = os.getenv("COGNODB_PASSWORD")

        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.username, self.password)
        )

    def verify_connection(self):
        self.driver.verify_connectivity()

    def close(self):
        self.driver.close()

    def run_query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]


db = Database()