import json

from flask import make_response, abort, request

from pplabel.config import db
from .model import Project
from .schema import ProjectSchema


def search():
    projects = Project.query.all()
    return ProjectSchema(many=True).dump(projects), 200


def get(project_id):
    project = Project.query.filter(Project.project_id == project_id).one_or_none()

    if project is not None:
        return ProjectSchema().dump(project)
    abort(404, f"Project not found for Id: {project_id}")


# TODO: add request id
def post():
    new_project = request.get_json()
    schema = ProjectSchema()
    new_project = schema.load(new_project)
    existing = Project.query.filter(Project.name == new_project.name).one_or_none()
    if existing is not None:
        abort(
            404,
            f"Project with name {new_project.name} already exists. Plz choose another name.",
        )
    db.session.add(new_project)
    db.session.commit()
    return schema.dump(new_project), 201


def put(project_id):
    # 1. check project exists
    project = Project.query.filter(Project.project_id == project_id).one_or_none()
    if project is None:
        abort(404, f"Project with project_id {project_id} is not found.")
    body = request.get_json()

    # 2. key in keys: change one property
    if "key" in body.keys():
        cols = [c.key for c in Project.__table__.columns]
        k, v = body["key"], body["value"]
        if k not in cols:
            abort(404, f"Project doesn't have property {k}")
        setattr(project, k, v)
        db.session.commit()
    else:
        # change all provided properties
        stmt = Project.query.filter(Project.project_id == project_id).update(body)
        db.session.commit()


    # FIXME: really need to requery?
    project = Project.query.filter(Project.project_id == project_id).one_or_none()
    return ProjectSchema().dump(project), 200


def delete(project_id):
    project = Project.query.filter(Project.project_id == project_id).one_or_none()

    if project is None:
        abort(404, f"Project {project_id} don't exist int the databae.")

    db.session.delete(project)
    db.session.commit()
    return make_response(f"Project {project_id} deleted", 200)