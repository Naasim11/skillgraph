import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("COGNODB_URI")
USERNAME = os.getenv("COGNODB_USERNAME")
PASSWORD = os.getenv("COGNODB_PASSWORD")

print("Connecting to:", URI)
print("Username:", USERNAME)

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

try:
    driver.verify_connectivity()
    print("SUCCESS: Connected to CognoDB!")

    with driver.session() as session:
        result = session.run(
            "RETURN 'SkillGraph connected!' AS message"
        )
        print(result.single()["message"])

except Exception as e:
    print("ERROR: Could not connect to CognoDB")
    print(type(e).__name__, e)

finally:
    driver.close()