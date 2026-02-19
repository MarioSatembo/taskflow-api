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


if __name__ == '__main__':
        app.run(debug=True)