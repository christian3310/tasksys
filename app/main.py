from flask import Flask, request

from app.managers import TaskManager
from app.models import Response


app = Flask(__name__)
task_manager = TaskManager()

@app.route('/')
def check_health():
    return 'healthy'

@app.route('/tasks')
def get_all_tasks():
    items = task_manager.get_all()
    resp = Response(result=items)
    return resp.dict()


@app.route('/task', methods=['POST'])
def create_task():
    data = request.get_json(force=True)
    result = task_manager.create(data)
    resp = Response(result=result)
    status_code = 200 if isinstance(result, task_manager.model) else 403
    return resp.dict(), status_code


@app.route('/task/<int:task_id>', methods=['PUT', 'DELETE'])
def modify_task(task_id):
    if request.method == 'PUT':
        data = request.get_json(force=True)
        result = task_manager.update(task_id, data)
        status_code = 201 if isinstance(result, task_manager.model) else 403
    elif request.method == 'DELETE':
        result = task_manager.delete(task_id)
        status_code = 200 if result == 'success' else 403

    resp = Response(result=result)
    return resp.dict(), status_code
