from flask import Blueprint, jsonify, request
from models import db, Task

routes = Blueprint('routes', __name__)

@routes.route("/tasks", methods=["GET"])
def get_task():
        tasks = Task.query.all()
        return jsonify([task.to_dict() for task in tasks])

@routes.route("/tasks", methods=["POST"])
def creat_task():
        data = request.get_json()
        new_task = Task(title=data["title"], done=data.get("done", False))
        db.session.add(new_task)
        db.session.commit()
        return jsonify(new_task.to_dict()), 201

@routes.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
        data = request.get_json
        task = Task.query.get(task_id)
        if task:
                task.title = data.get("title", task.title)
                task.done = data.get("done", task.done)
                db.session.commit()
                return jsonify({"error": "Tarefa nao encontrada"}), 404
        
@routes.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
        task = Task.query.get(task_id)
        if task:
                db.session.delete(task)
                db.session.commit()
                return jsonify({"message": "Tarefa deteltada com sucesso!"})
        return jsonify({"error": "Tarefa nao encontrada"})