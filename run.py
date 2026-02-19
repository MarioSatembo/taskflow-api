from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


# tasks = [
#         {"id": 1, "title": "Learn Flask", 'done': False},
#         {"id": 2, "title": "Study C#", 'done': True},
#  ]

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(200), nullable=False)
        done = db.Column(db.Boolean, default=False)

        def to_dict(self):
                return {"id": self.id, "title": self.title, "done": self.done}

with app.app_context():
        db.create_all()


@app.route("/")
def home():
        return 'API TaskFlow is Working'


@app.route("/tasks", methods=["GET"])
def get_tasks():
        tasks = Task.query.all()
        return jsonify([task.to_dict() for task in tasks])


@app.route("/tasks", methods=["POST"])
def create_task():
        # new_task = request.get_json()
        # new_task["id"] = len(tasks) + 1
        # tasks.append(new_task)

        # return jsonify(new_task), 201
        data = request.get_json()
        new_task = Task(title=data["title"], done=data.get("done", False))
        db.session.add(new_task)
        db.session.commit()
        
        return jsonify(new_task.to_dict()), 201
        

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
        # task_data = request.get_json()
        # for task in tasks:
        #       if task["id"] == task_id:
        #                task["title"] = task_data.get("title", task["title"])
        #                task["done"] = task_data.get("done", task["done"])
        #        return jsonify(task)
        # return jsonify({"error": "Tarefa nao encontrada"}), 404

        data = request.get_json()
        task = Task.query.get(task_id)
        if task:
                task.title = data.get("title", task.title)
                task.done = data.get("done", task.done)
                db.session.commit()
                return jsonify(task.to_dict())
        return jsonify({"error": "Tarefa nao encontrada"})

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
        # for task in tasks:
        #         if task["id"] == task_id:
        #                 tasks.remove(task)
        #                 return jsonify({"message": f"Tarefa {task_id} deletada com sucesso"})
        # return jsonify({"error": "Tarefa n'ao encontrada"})

        task = Task.query.get(task_id)
        if task:
                db.session.delete(task)
                db.session.commit()
                return jsonify({"message": f"Tarefa {task_id} deletada com sucesso!"})
        return jsonify({"error": "Tarefa nao encontrada"}, 404)

if __name__ == '__main__':
        app.run(debug=True)