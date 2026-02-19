from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = [
        {"id": 1, "title": "Learn Flask", 'done': False},
        {"id": 2, "title": "Study C#", 'done': True},
]

@app.route("/")
def home():
        return 'API TaskFlow is Working'


@app.route("/tasks", methods=["GET"])
def get_tasks():
        return jsonify(tasks)


@app.route("/tasks", methods=["POST"])
def create_task():
        new_task = request.get_json()
        new_task["id"] = len(tasks) + 1
        tasks.append(new_task)
        
        return jsonify(new_task), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
        task_data = request.get_json()
        for task in tasks:
                if task["id"] == task_id:
                        task["title"] = task_data.get("title", task["title"])
                        task["done"] = task_data.get("done", task["done"])
                return jsonify(task)
        return jsonify({"error": "Tarefa nao encontrada"}), 404

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
        for task in tasks:
                if task["id"] == task_id:
                        tasks.remove(task)
                        return jsonify({"message": f"Tarefa {task_id} deletada com sucesso"})
        return jsonify({"error": "Tarefa n'ao encontrada"})

if __name__ == '__main__':
        app.run(debug=True)