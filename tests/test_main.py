class TestGetAllTasks:
    endpoint = '/tasks'

    def test_empty_tasks(self, client):
        resp = client.get(self.endpoint)
        assert resp.content_type == 'application/json'
        assert resp.get_json() == {'result': []}
  
    def test_all_tasks(self, client, fulfill_tasks):
        resp = client.get(self.endpoint)
        result = resp.get_json()
        for i, task in enumerate(fulfill_tasks):
            assert result['result'][i] == task.dict()

        assert resp.content_type == 'application/json'


class TestCreateTask:
    endpoint = '/task'
    
    def test_create_successfully(self, client, task_manager_):
        resp = client.post(self.endpoint, json={'name': 'success_test'})
        result = resp.get_json()
        task = task_manager_.get(result['result']['id'])
        assert resp.status_code == 200
        assert resp.content_type == 'application/json'
        assert result['result'] == task.dict()

    def test_create_failed(self, client):
        resp = client.post(self.endpoint, json={'status': 0})
        result = resp.get_json()
        assert resp.status_code == 403
        assert resp.content_type == 'application/json'
        assert result['result'].startswith('1 validation error')


class TestModifyTask:
    endpoint = '/task/{task_id}'

    def test_update_task(self, client, fulfill_tasks, task_manager_):
        task = fulfill_tasks[0].dict()
        task['status'] = 1
        endpoint = self.endpoint.format(task_id=task['id'])

        resp = client.put(endpoint, json=task)
        result = resp.get_json()
        new_task = task_manager_.get(task['id'])
        assert resp.status_code == 201
        assert resp.content_type == 'application/json'
        assert result['result'] == new_task.dict()
    
    def test_update_task_with_wrong_id(self, client, fulfill_tasks):
        task = fulfill_tasks[1].dict()
        task['id'] += 1
        task['status'] = 1
        endpoint = self.endpoint.format(task_id=fulfill_tasks[1].id)

        resp = client.put(endpoint, json=task)
        result = resp.get_json()
        assert resp.status_code == 403
        assert resp.content_type == 'application/json'
        assert result['result'] == f'invalid updating on Task <{fulfill_tasks[1].id}>'

    def test_update_missing_task(self, client, fulfill_tasks):
        task = fulfill_tasks[2].dict()
        task['id'] += 20
        endpoint = self.endpoint.format(task_id=task['id'])

        resp = client.put(endpoint, json=task)
        result = resp.get_json()
        assert resp.status_code == 403
        assert resp.content_type == 'application/json'
        assert result['result'] == f'Task <{task["id"]}> does not exist'

    def test_delete_successfully(self, client, fulfill_tasks):
        task = fulfill_tasks[0]
        endpoint = self.endpoint.format(task_id=task.id)

        resp = client.delete(endpoint)
        result = resp.get_json()
        assert resp.status_code == 200
        assert resp.content_type == 'application/json'
        assert result['result'] == 'success'

    def test_delete_failed(self, client, fulfill_tasks):
        task = fulfill_tasks[-1]
        endpoint = self.endpoint.format(task_id=task.id+30)

        resp = client.delete(endpoint)
        result = resp.get_json()
        assert resp.status_code == 403
        assert resp.content_type == 'application/json'
        assert result['result'] == 'failure'
