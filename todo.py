from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'todos.json'

def load_todos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_todos(todos):
    with open(DATA_FILE, 'w') as f:
        json.dump(todos, f, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(load_todos())

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    title = data.get('title', '').strip()
    if not title:
        return jsonify({'error': 'Title is required'}), 400

    todos = load_todos()
    new_todo = {
        'id': max([t['id'] for t in todos], default=0) + 1,
        'title': title,
        'description': data.get('description', '').strip(),
        'priority': data.get('priority', 'medium'),
        'done': False,
        'created_at': datetime.now().strftime('%d %b %Y')
    }
    todos.append(new_todo)
    save_todos(todos)
    return jsonify(new_todo), 201

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    todos = load_todos()
    todo = next((t for t in todos if t['id'] == todo_id), None)
    if not todo:
        return jsonify({'error': 'Task not found'}), 404

    if 'title' in data:
        title = data['title'].strip()
        if not title:
            return jsonify({'error': 'Title is required'}), 400
        todo['title'] = title
    if 'description' in data:
        todo['description'] = data['description'].strip()
    if 'priority' in data:
        todo['priority'] = data['priority']
    if 'done' in data:
        todo['done'] = data['done']

    save_todos(todos)
    return jsonify(todo)

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todos = load_todos()
    updated = [t for t in todos if t['id'] != todo_id]
    if len(updated) == len(todos):
        return jsonify({'error': 'Task not found'}), 404
    save_todos(updated)
    return jsonify({'message': 'Deleted'})

if __name__ == '__main__':
    app.run(debug=True)
