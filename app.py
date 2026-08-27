from flask import Flask, render_template, request
from database import db
from queries import (
    get_all_jobs,
    get_all_skills,
    get_person_skills,
    get_matching_jobs,
    get_job_skills,
    get_skill_connections,
    get_graph_data,
)

app = Flask(__name__)


@app.route("/")
def home():
    try:
        jobs = get_all_jobs()
        skills = get_all_skills()
        person_skills = get_person_skills("Naasim")
        matches = get_matching_jobs("Naasim")

        return render_template(
            "index.html",
            jobs=jobs,
            skills=skills,
            person_skills=person_skills,
            matches=matches,
            error=None,
        )

    except Exception as e:
        return render_template(
            "index.html",
            jobs=[],
            skills=[],
            person_skills=[],
            matches=[],
            error="Unable to connect to the graph database.",
        ), 503


@app.route("/job/<job_title>")
def job_details(job_title):
    try:
        job_skills = get_job_skills(job_title)

        return render_template(
            "job.html",
            job_title=job_title,
            job_skills=job_skills,
            error=None,
        )

    except Exception:
        return render_template(
            "job.html",
            job_title=job_title,
            job_skills=[],
            error="Unable to load job details.",
        ), 503
@app.route("/skill/<skill_name>")
def skill_details(skill_name):
    try:
        connections = get_skill_connections(skill_name)

        return render_template(
            "skill.html",
            skill_name=skill_name,
            connections=connections,
            error=None,
        )

    except Exception:
        return render_template(
            "skill.html",
            skill_name=skill_name,
            connections=[],
            error="Unable to load skill connections.",
        ), 503@app.route("/skill/<skill_name>")
@app.route("/graph/<skill_name>")
def graph_explorer(skill_name):
    try:
        graph_data = get_graph_data(skill_name)

        return render_template(
            "graph.html",
            skill_name=skill_name,
            graph_data=graph_data,
            error=None,
        )

    except Exception:
        return render_template(
            "graph.html",
            skill_name=skill_name,
            graph_data=[],
            error="Unable to load graph data.",
        ), 503
if __name__ == "__main__":
    app.run(debug=True)