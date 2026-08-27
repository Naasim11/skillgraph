from database import db


def get_all_skills():
    query = """
    MATCH (s:Skill)
    RETURN s.name AS name, s.category AS category
    ORDER BY s.name
    """
    return db.run_query(query)


def get_all_jobs():
    query = """
    MATCH (j:Job)
    RETURN j.title AS title, j.category AS category
    ORDER BY j.title
    """
    return db.run_query(query)


def get_job_skills(job_title):
    query = """
    MATCH (j:Job {title: $job_title})-[:REQUIRES]->(s:Skill)
    RETURN j.title AS job, s.name AS skill, s.category AS category
    ORDER BY s.name
    """
    return db.run_query(query, {"job_title": job_title})


def get_person_skills(person_name):
    query = """
    MATCH (p:Person {name: $person_name})-[:HAS_SKILL]->(s:Skill)
    RETURN p.name AS person, s.name AS skill, s.category AS category
    ORDER BY s.name
    """
    return db.run_query(query, {"person_name": person_name})


def get_matching_jobs(person_name):
    query = """
    MATCH (p:Person {name: $person_name})-[:HAS_SKILL]->(s:Skill)
    MATCH (j:Job)-[:REQUIRES]->(s)
    WITH p, j, COUNT(DISTINCT s) AS matched_skills
    MATCH (j)-[:REQUIRES]->(required:Skill)
    WITH p, j, matched_skills, COUNT(DISTINCT required) AS total_skills
    RETURN
        j.title AS job,
        matched_skills,
        total_skills,
        100.0 * matched_skills / total_skills AS match_percentage
    ORDER BY match_percentage DESC
    """
    return db.run_query(query, {"person_name": person_name})

def get_skill_connections(skill_name):
    query = """
    MATCH (s:Skill {name: $skill_name})
    MATCH (s)<-[:REQUIRES]-(j:Job)-[:REQUIRES]->(related:Skill)
    WHERE related.name <> s.name
    RETURN
        s.name AS skill,
        related.name AS related_skill,
        COUNT(DISTINCT j) AS shared_jobs
    ORDER BY shared_jobs DESC, related_skill
    """
    return db.run_query(query, {"skill_name": skill_name})
def get_graph_data(skill_name):
    query = """
    MATCH (s:Skill {name: $skill_name})

    OPTIONAL MATCH (s)<-[:REQUIRES]-(j:Job)

    OPTIONAL MATCH (j)-[:REQUIRES]->(related:Skill)
    WHERE related.name <> s.name

    RETURN
        s.name AS skill,
        collect(DISTINCT {
            name: j.title,
            type: "Job"
        }) AS jobs,
        collect(DISTINCT {
            name: related.name,
            type: "Skill"
        }) AS related_skills
    """

    return db.run_query(query, {"skill_name": skill_name})