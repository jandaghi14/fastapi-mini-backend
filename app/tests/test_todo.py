import uuid


def test_pagination_user(client, create_user, create_a_todo, auth_header):
    headers = auth_header('test1user', 'randompassword', 'user')

    create_a_todo(headers=headers)
    create_a_todo(headers=headers)
    create_a_todo(headers=headers)
    create_a_todo(headers=headers)
    create_a_todo(headers=headers)

    response = client.get('/todos/get_all_todos',
                          headers=headers
                          )
    assert response.status_code == 200
    assert len(response.json()) == 5

    response = client.get('/todos/get_all_todos',
                          params={'limit': 3,
                                  'offset': 1},
                          headers=headers
                          )
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_pagination_admin(client, create_a_todo, auth_header, only_get_token, create_user):
    admin_headers = auth_header('usertestadmin', 'randompasswordadmin', 'admin')

    username = uuid.uuid4().hex[:6]
    user = create_user(username, 'randompassword', 'user')

    token = only_get_token(username, 'randompassword')
    user_headers = {"Authorization": f"Bearer {token}"}
    user_id = user['id']

    create_a_todo(headers=user_headers)
    create_a_todo(headers=user_headers)
    create_a_todo(headers=user_headers)
    create_a_todo(headers=user_headers)
    create_a_todo(headers=user_headers)

    response = client.get(f'/admin/get_all_todos/{user_id}',
                          headers=admin_headers,

                          )
    assert response.status_code == 200
    assert len(response.json()) == 5

    response = client.get(f'/admin/get_all_todos/{user_id}',
                          params={'limit': 3,
                                  'offset': 1},
                          headers=admin_headers
                          )
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_create_todo_title_too_short(client, auth_header):
    user = auth_header('usertest1', 'randompass', 'user')
    response = client.post('/todos/create_todo', json={
        'title': 'qw',
        'description': 'description',
        'priority': 'low'},
        headers=user)
    assert response.status_code == 422


def test_get_all_todos_with_owner(client, auth_header, create_a_todo):
    header = auth_header('test1username', 'randompass', 'user')
    create_a_todo(headers=header)
    response = client.get('/todos/get_all_todo_with_username', headers=header)
    assert response.status_code == 200
    assert response.json()[0]['owner']['username'] == 'test1username'


def test_updated_at_changes_on_update(auth_header, create_a_todo, client, create_user, only_get_token):
    import time

    username = uuid.uuid4().hex[:6]
    create_user(username, 'randompassword', 'user')

    token = only_get_token(username, 'randompassword')
    user_headers = {"Authorization": f"Bearer {token}"}

    todo = create_a_todo(headers=user_headers)
    todo_id = todo['id']
    original_updated_at = todo['updated_at']

    time_to_sleep = 1
    time.sleep(time_to_sleep)
    new_updated_todo = {
        "title": "updatedString",
        "description": "updateddescription",
        "status": "pending",
        "priority": "low",
        "due_date": "2026-05-06T13:33:46.721Z"
    }

    response = client.put(f'/todos/update_todo/{todo_id}', headers=user_headers, json=new_updated_todo)

    assert response.status_code == 200
    assert response.json()['updated_at'] != original_updated_at


def test_user_update_todo_success(client, create_user, create_a_todo, only_get_token):
    user1_username = f"user_{uuid.uuid4().hex[:6]}"
    user1_password = 'randompass'
    role = 'user'
    create_user(username=user1_username, password=user1_password, role=role)

    token_user1 = only_get_token(user1_username, user1_password)
    headers_user1 = {"Authorization": f"Bearer {token_user1}"}

    todo1 = create_a_todo(title='testtitletodo1', headers=headers_user1)
    todo1_id = todo1['id']

    new_updated_todo = {
        "title": "updatedString",
        "description": "updateddescription",
        "status": "pending",
        "priority": "low",
        "due_date": "2026-05-06T13:33:46.721Z"
    }
    response = client.put(f'/todos/update_todo/{todo1_id}', json=new_updated_todo, headers=headers_user1)

    assert response.status_code == 200
    assert response.json()['title'] == 'updatedString'
    assert response.json()['description'] == 'updateddescription'
    assert response.json()['status'] == 'pending'


def test_user_update_other_user_todo_forbidden(client, create_user, create_a_todo, only_get_token):
    user1_username = f"user_{uuid.uuid4().hex[:6]}"
    user1_password = 'randompass'
    role1 = 'user'
    create_user(username=user1_username, password=user1_password, role=role1)

    token_user1 = only_get_token(user1_username, user1_password)
    headers_user1 = {"Authorization": f"Bearer {token_user1}"}

    todo1 = create_a_todo(title='testtitletodo1', headers=headers_user1)
    todo1_id = todo1['id']

    user2_username = f"user_{uuid.uuid4().hex[:6]}"
    user2_password = 'randompass'
    role2 = 'user'
    create_user(username=user2_username, password=user2_password, role=role2)

    token_user2 = only_get_token(user2_username, user2_password)
    headers_user2 = {"Authorization": f"Bearer {token_user2}"}

    new_updated_todo = {
        "title": "updatedString",
        "description": "updateddescription",
        "status": "pending",
        "priority": "low",
        "due_date": "2026-05-06T13:33:46.721Z"
    }
    response = client.put(f'/todos/update_todo/{todo1_id}', json=new_updated_todo, headers=headers_user2)

    assert response.status_code == 403


def test_user_soft_delete_a_todo(client, create_user, create_a_todo, only_get_token):
    user1_username = f"user_{uuid.uuid4().hex[:6]}"
    user1_password = 'randompass'
    role1 = 'user'
    create_user(username=user1_username, password=user1_password, role=role1)

    token_user1 = only_get_token(user1_username, user1_password)
    headers_user1 = {"Authorization": f"Bearer {token_user1}"}

    todo1 = create_a_todo(title='testtitletodo1', headers=headers_user1)
    todo1_id = todo1['id']

    response1 = client.get(f'/todos/get_todo_by_id/{todo1_id}', headers=headers_user1)
    assert response1.status_code == 200
    assert response1.json()['id'] == todo1_id

    client.delete(f'/todos/delete_todo/{todo1_id}', headers=headers_user1)

    response = client.get(f'/todos/get_todo_by_id/{todo1_id}', headers=headers_user1)

    assert response.status_code == 404
    assert response.json()['detail'] == "Todo not found"


def test_get_todo_by_id(client, create_user, create_a_todo, only_get_token):
    user1_username = f"user_{uuid.uuid4().hex[:6]}"
    user1_password = 'randompass'
    role1 = 'user'
    create_user(username=user1_username, password=user1_password, role=role1)

    token_user1 = only_get_token(user1_username, user1_password)
    headers_user1 = {"Authorization": f"Bearer {token_user1}"}

    todo1 = create_a_todo(title='testtitletodo1', headers=headers_user1)
    todo1_id = todo1['id']

    response1 = client.get(f'/todos/get_todo_by_id/{todo1_id}', headers=headers_user1)
    assert response1.status_code == 200
    assert response1.json()['id'] == todo1_id


def test_get_todo_by_id_forbiden(client, create_user, create_a_todo, only_get_token):
    user1_username = f"user_{uuid.uuid4().hex[:6]}"
    user1_password = 'randompass'
    role1 = 'user'
    create_user(username=user1_username, password=user1_password, role=role1)

    token_user1 = only_get_token(user1_username, user1_password)
    headers_user1 = {"Authorization": f"Bearer {token_user1}"}

    todo1 = create_a_todo(title='testtitletodo1', headers=headers_user1)
    todo1_id = todo1['id']

    user2_username = f"user_{uuid.uuid4().hex[:6]}"
    user2_password = 'randompass'
    role2 = 'user'
    create_user(username=user2_username, password=user2_password, role=role2)

    token_user2 = only_get_token(user2_username, user2_password)
    headers_user2 = {"Authorization": f"Bearer {token_user2}"}
    response1 = client.get(f'/todos/get_todo_by_id/{todo1_id}', headers=headers_user2)
    assert response1.status_code == 403


def test_get_all_todos_with_due_date_success(client, create_user, create_a_todo, only_get_token):
    user1_username = f"user_{uuid.uuid4().hex[:6]}"
    user1_password = 'randompass'
    role = 'user'
    create_user(username=user1_username, password=user1_password, role=role)

    token_user1 = only_get_token(user1_username, user1_password)
    headers_user1 = {"Authorization": f"Bearer {token_user1}"}

    create_a_todo(title='testtitletodo1', headers=headers_user1)
    create_a_todo(title='testtitletodo2', headers=headers_user1)

    todo3 = create_a_todo(title='testtitletodo3', headers=headers_user1)
    todo_id3 = todo3['id']
    todo4 = create_a_todo(title='testtitletodo4', headers=headers_user1)
    todo_id4 = todo4['id']

    new_updated_todo = {
        "due_date": "2026-05-22T13:33:46.721Z"
    }
    client.put(f'/todos/update_todo/{todo_id3}', json=new_updated_todo, headers=headers_user1)
    client.put(f'/todos/update_todo/{todo_id4}', json=new_updated_todo, headers=headers_user1)

    response = client.get("/todos/get_all_todos",
                          params={'due_date_from': '2026-05-22'},
                          headers=headers_user1
                          )
    assert len(response.json()) == 2
    assert response.status_code == 200


def test_get_all_todos_without_due_date(client, create_user, create_a_todo, only_get_token):
    user1_username = f"user_{uuid.uuid4().hex[:6]}"
    user1_password = 'randompass'
    role = 'user'
    create_user(username=user1_username, password=user1_password, role=role)

    token_user1 = only_get_token(user1_username, user1_password)
    headers_user1 = {"Authorization": f"Bearer {token_user1}"}

    create_a_todo(title='testtitletodo1', headers=headers_user1)
    create_a_todo(title='testtitletodo2', headers=headers_user1)

    todo3 = create_a_todo(title='testtitletodo3', headers=headers_user1)
    todo_id3 = todo3['id']
    todo4 = create_a_todo(title='testtitletodo4', headers=headers_user1)
    todo_id4 = todo4['id']

    new_updated_todo = {
        "due_date": "2026-05-22T13:33:46.721Z"
    }
    client.put(f'/todos/update_todo/{todo_id3}', json=new_updated_todo, headers=headers_user1)
    client.put(f'/todos/update_todo/{todo_id4}', json=new_updated_todo, headers=headers_user1)

    response = client.get('/todos/get_all_todos', headers=headers_user1)
    assert len(response.json()) == 4
    assert response.status_code == 200


def test_get_all_todos_with_due_date__with_owner_success(client, create_user, create_a_todo, only_get_token):
    user1_username = f"user_{uuid.uuid4().hex[:6]}"
    user1_password = 'randompass'
    role = 'user'
    create_user(username=user1_username, password=user1_password, role=role)

    token_user1 = only_get_token(user1_username, user1_password)
    headers_user1 = {"Authorization": f"Bearer {token_user1}"}

    create_a_todo(title='testtitletodo1', headers=headers_user1)
    create_a_todo(title='testtitletodo2', headers=headers_user1)

    todo3 = create_a_todo(title='testtitletodo3', headers=headers_user1)
    todo_id3 = todo3['id']
    todo4 = create_a_todo(title='testtitletodo4', headers=headers_user1)
    todo_id4 = todo4['id']

    new_updated_todo = {
        "due_date": "2026-05-22T13:33:46.721Z"
    }
    client.put(f'/todos/update_todo/{todo_id3}', json=new_updated_todo, headers=headers_user1)
    client.put(f'/todos/update_todo/{todo_id4}', json=new_updated_todo, headers=headers_user1)

    response = client.get('/todos/get_all_todo_with_username',
                          params={'due_date_from': '2026-05-22'},
                          headers=headers_user1
                          )
    assert len(response.json()) == 2
    assert response.status_code == 200
    assert response.json()[0]['owner']['username'] == user1_username


def test_get_all_todos_without_due_date_with_owner_(client, create_user, create_a_todo, only_get_token):
    user1_username = f"user_{uuid.uuid4().hex[:6]}"
    user1_password = 'randompass'
    role = 'user'
    create_user(username=user1_username, password=user1_password, role=role)

    token_user1 = only_get_token(user1_username, user1_password)
    headers_user1 = {"Authorization": f"Bearer {token_user1}"}

    create_a_todo(title='testtitletodo1', headers=headers_user1)
    create_a_todo(title='testtitletodo2', headers=headers_user1)

    todo3 = create_a_todo(title='testtitletodo3', headers=headers_user1)
    todo_id3 = todo3['id']
    todo4 = create_a_todo(title='testtitletodo4', headers=headers_user1)
    todo_id4 = todo4['id']

    new_updated_todo = {
        "due_date": "2026-05-22T13:33:46.721Z"
    }
    client.put(f'/todos/update_todo/{todo_id3}', json=new_updated_todo, headers=headers_user1)
    client.put(f'/todos/update_todo/{todo_id4}', json=new_updated_todo, headers=headers_user1)

    response = client.get('/todos/get_all_todo_with_username', headers=headers_user1)
    assert len(response.json()) == 4
    assert response.status_code == 200
    assert response.json()[0]['owner']['username'] == user1_username
