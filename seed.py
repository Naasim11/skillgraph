from database import db


def seed_database():
    # Clear existing data
    db.run_query("MATCH (n) DETACH DELETE n")

    # Create skills
    skills = [
        ("Python", "Programming"),
        ("SQL", "Database"),
        ("Java", "Programming"),
        ("HTML", "Web Development"),
        ("CSS", "Web Development"),
        ("JavaScript", "Web Development"),
        ("Git", "Tools"),
        ("Flask", "Backend"),
        ("Spring Boot", "Backend"),
        ("MongoDB", "Database"),
    ]

    for name, category in skills:
        db.run_query(
            """
            MERGE (s:Skill {name: $name})
            SET s.category = $category
            """,
            {"name": name, "category": category}
        )

    # Create jobs
    jobs = [
        ("Python Developer", "Software Development"),
        ("Java Developer", "Software Development"),
        ("Full Stack Developer", "Software Development"),
        ("Backend Developer", "Software Development"),
        ("Data Analyst", "Data"),
    ]

    for title, category in jobs:
        db.run_query(
            """
            MERGE (j:Job {title: $title})
            SET j.category = $category
            """,
            {"title": title, "category": category}
        )

    # Create skill relationships for jobs
    job_skills = {
        "Python Developer": ["Python", "SQL", "Git", "Flask"],
        "Java Developer": ["Java", "SQL", "Git", "Spring Boot"],
        "Full Stack Developer": [
            "HTML",
            "CSS",
            "JavaScript",
            "Python",
            "MongoDB",
            "Git",
        ],
        "Backend Developer": ["Python", "SQL", "Flask", "MongoDB", "Git"],
        "Data Analyst": ["Python", "SQL", "Git"],
    }

    for job_title, skill_names in job_skills.items():
        for skill_name in skill_names:
            db.run_query(
                """
                MATCH (j:Job {title: $job_title})
                MATCH (s:Skill {name: $skill_name})
                MERGE (j)-[:REQUIRES]->(s)
                """,
                {
                    "job_title": job_title,
                    "skill_name": skill_name,
                }
            )

    # Create a sample person
    db.run_query(
        """
        MERGE (p:Person {name: $name})
        SET p.role = $role
        """,
        {
            "name": "Naasim",
            "role": "CSE Fresher",
        }
    )

    # Add skills to person
    person_skills = ["Python", "SQL", "Java", "HTML", "CSS", "Git"]

    for skill_name in person_skills:
        db.run_query(
            """
            MATCH (p:Person {name: $person_name})
            MATCH (s:Skill {name: $skill_name})
            MERGE (p)-[:HAS_SKILL]->(s)
            """,
            {
                "person_name": "Naasim",
                "skill_name": skill_name,
            }
        )

    print("Database seeded successfully!")


if __name__ == "__main__":
    try:
        db.verify_connection()
        seed_database()
    finally:
        db.close()