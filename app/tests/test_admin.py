import uuid

def test_admin_panel(client):
    client.post(
        '/register', 
        json={
            "username": "useradmin",
            "password" : "user1password",
            "role" : "admin"})
    
    login_response = client.post('/login', data={
            "username": "useradmin",
            "password" : "user1password"})
    
    token = login_response.json()['access_token']
    
    response = client.get('/admin',headers={
        'Authorization' : f"Bearer {token}"
    }) 
    assert response.status_code == 200   
    assert response.json()['message'] == 'Welcome admin'
    
    
def test_admin_hard_delete_todo_success(client, auth_header,create_a_todo):
    headers = auth_header('useradmin2', 'passwordadmin', 'admin')
    
    todo =create_a_todo(title = 'testtitletodo', headers = headers)
    
    response = client.delete(
        f"/admin/hard_delete_todo/{todo['id']}",
        headers = headers)
    
    assert response.status_code == 200
    assert 'Todo by ID' in response.json()['message']
    
    response2 = client.get(f'/todos/get_todo_by_id/{todo['id']}',headers = headers)
    assert response2.status_code == 404
    assert response2.json()['detail'] == "Todo not found"
    
    
def test_admin_hard_delete_todo_not_found_todo(client, auth_header,create_a_todo):
    username = f"user_{uuid.uuid4().hex[:6]}"
    headers = auth_header(username= username,password= 'passwordadmin',role = 'admin')
    
    todo =create_a_todo(title = 'testtitletodo', headers = headers)

    client.delete(
        f"/admin/hard_delete_todo/{todo['id']}",
        headers = headers)
    
    response = client.delete(
        f"/admin/hard_delete_todo/{todo['id']}",
        headers = headers)
    
    assert response.status_code == 404
    assert response.json()['detail'] == "Todo not found"
def test_admin_hard_delete_todo_non_admin_user(client, auth_header,create_a_todo):

    username = f"user_{uuid.uuid4().hex[:6]}"
    headers = auth_header(username= username, password= 'adminpassword',role = 'admin')
    
    todo =create_a_todo(title = 'testtitletodo', headers = headers)
    
    username = f"user_{uuid.uuid4().hex[:6]}"
    headers2 = auth_header(username= username, password= 'randompassword',role = 'user')

    response = client.delete(
        f'/admin/hard_delete_todo/{todo['id']}',
        headers = headers2)
    
    assert response.status_code == 403
    assert response.json()['detail'] == "Not authorized!"
def test_admin_hard_delete_todo_unauthorized(client, auth_header,create_a_todo):

    username = f"user_{uuid.uuid4().hex[:6]}"
    headers = auth_header(username= username, password= 'passwordadmin',role = 'user')
    
    todo =create_a_todo(title = 'testtitletodo', headers = headers)
    
    response = client.delete(
        f"/admin/hard_delete_todo/{todo['id']}" )
    
    assert response.status_code == 401
    assert response.json()['detail'] == 'Not authenticated'

#---------------------------------------------------------------------------------------------

def test_admin_delete_user_success(client,auth_header,create_user):
    username_admin = f"user_{uuid.uuid4().hex[:6]}"
    headers = auth_header(username= username_admin,password= 'passwordadmin',role = 'admin')

    username1 = f"user_{uuid.uuid4().hex[:6]}"
    user1 = create_user(username = username1, password = "user1password", role = 'user')
    user1_id = user1['id']
    
    response = client.delete(f"/admin/delete_user/{user1_id}", headers=headers)

    assert response.status_code == 200
    assert response.json()['message'] == f"User {username1} with ID {user1_id} deleted successfully! "
    
def test_admin_delete_user_not_found(client,auth_header,create_user):
    username_admin = f"user_{uuid.uuid4().hex[:6]}"
    headers = auth_header(username= username_admin,password= 'passwordadmin',role = 'admin')

    username1 = f"user_{uuid.uuid4().hex[:6]}"
    user1 = create_user(username = username1, password = "user1password", role = 'user')
    user1_id = user1['id']
    
    client.delete(f"/admin/delete_user/{user1_id}", headers=headers)

    response = client.delete(f"/admin/delete_user/{user1_id}", headers=headers)
    
    assert response.status_code == 404
    assert response.json()['detail'] == "User not found"
def test_admin_delete_user_non_admin_user(client,auth_header,create_user):
    username0 = f"user_{uuid.uuid4().hex[:6]}"
    headers = auth_header(username= username0,password= 'user1password',role = 'user')

    username1 = f"user_{uuid.uuid4().hex[:6]}"
    user1 = create_user(username = username1, password = "user2password", role = 'user')
    user1_id = user1['id']
    
    response = client.delete(f"/admin/delete_user/{user1_id}", headers=headers)
    
    assert response.status_code == 403
    assert response.json()['detail'] == "Not authorized!"
def test_admin_delete_user_unauthorized(client,auth_header,create_user):
    username0 = f"user_{uuid.uuid4().hex[:6]}"
    headers = auth_header(username= username0,password= 'user1password',role = 'user')

    username1 = f"user_{uuid.uuid4().hex[:6]}"
    user1 = create_user(username = username1, password = "user2password", role = 'user')
    user1_id = user1['id']
    
    response = client.delete(f"/admin/delete_user/{user1_id}")
    
    assert response.status_code == 401
    assert response.json()['detail'] == "Not authenticated"
def test_admin_delete_user_admin(client,auth_header,create_user):
    admin1_username = f"user_{uuid.uuid4().hex[:6]}"
    headers = auth_header(username= admin1_username,password= 'user1password',role = 'admin')

    admin2_username = f"user_{uuid.uuid4().hex[:6]}"
    user1 = create_user(username = admin2_username, password = "user2password", role = 'admin')
    user1_id = user1['id']
    
    response = client.delete(f"/admin/delete_user/{user1_id}",headers=headers)
    
    assert response.status_code == 403
    assert response.json()['detail'] == "!!!Admin users cannot be deleted!!!"

#---------------------------------------------------------------------------------------------

def test_admin_get_other_user_all_todos_success(client,auth_header,create_user,create_a_todo,only_get_token):
    
    admin1_username = f"user_{uuid.uuid4().hex[:6]}"
    headers_admin = auth_header(username= admin1_username,password= 'admin1password',role = 'admin')
    
    user_username = f"user_{uuid.uuid4().hex[:6]}"
    user_password = 'randompass'
    role = 'user'
    user1 = create_user(username = user_username, password = user_password, role = role)
    user_id = user1['id']

    token_user = only_get_token(user_username, user_password)
    headers_user1 = {"Authorization" : f"Bearer {token_user}"}
    
    todo1 =create_a_todo(title = 'testtitletodo1', headers = headers_user1)
    todo2 =create_a_todo(title = 'testtitletodo2', headers = headers_user1)

    response = client.get(f"/admin/get_all_todos/{user_id}", headers=headers_admin)

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]['title'] == 'testtitletodo1'
    assert response.json()[1]['title'] == 'testtitletodo2'
    
def test_admin_get_other_user_all_todos_not_found_user(client,auth_header,create_user,create_a_todo,only_get_token):
    
    admin1_username = f"user_{uuid.uuid4().hex[:6]}"
    headers_admin = auth_header(username= admin1_username,password= 'admin1password',role = 'admin')

    response = client.get(f"/admin/get_all_todos/{999999999}", headers=headers_admin)

    assert response.status_code == 404
    assert response.json()['detail'] == 'User not found'

def test_admin_get_other_user_all_todos_no_todos(client,auth_header,create_user,create_a_todo,only_get_token):
    
    admin1_username = f"user_{uuid.uuid4().hex[:6]}"
    headers_admin = auth_header(username= admin1_username,password= 'admin1password',role = 'admin')
    
    user_username = f"user_{uuid.uuid4().hex[:6]}"
    user_password = 'randompass'
    role = 'user'
    user1 = create_user(username = user_username, password = user_password, role = role)
    user_id = user1['id']

    response = client.get(f"/admin/get_all_todos/{user_id}", headers=headers_admin)

    assert response.status_code == 200
    assert len(response.json()) == 0

def test_admin_get_other_user_all_todos_non_admin_user(client,auth_header,create_user,create_a_todo,only_get_token):
    
    user1_username = f"user_{uuid.uuid4().hex[:6]}"
    user1_password = 'randompass'
    role = 'user'
    user1 = create_user(username = user1_username, password = user1_password, role = role)
    user1_id = user1['id']
    
    token_user1 = only_get_token(user1_username, user1_password)
    headers_user1 = {"Authorization" : f"Bearer {token_user1}"}
    
    
    user2_username = f"user_{uuid.uuid4().hex[:6]}"
    user2_password = 'randompass'
    role = 'user'
    user2 = create_user(username = user2_username, password = user2_password, role = role)
    user2_id = user2['id']
    
    token_user2 = only_get_token(user2_username, user2_password)
    headers_user2 = {"Authorization" : f"Bearer {token_user2}"}
    
    todo1 =create_a_todo(title = 'testtitletodo1', headers = headers_user1)
    todo2 =create_a_todo(title = 'testtitletodo2', headers = headers_user1)
    
    

    response = client.get(f"/admin/get_all_todos/{user1_id}", headers=headers_user2)

    assert response.status_code == 403
    assert response.json()['detail'] == "Not authorized!"
    
def test_admin_can_see_soft_deleted_todos(client,auth_header,create_user,create_a_todo,only_get_token):
    
    admin1_username = f"user_{uuid.uuid4().hex[:6]}"
    headers_admin = auth_header(username= admin1_username,password= 'admin1password',role = 'admin')
    
    user_username = f"user_{uuid.uuid4().hex[:6]}"
    user_password = 'randompass'
    role = 'user'
    user1 = create_user(username = user_username, password = user_password, role = role)
    user_id = user1['id']

    token_user = only_get_token(user_username, user_password)
    headers_user1 = {"Authorization" : f"Bearer {token_user}"}
    
    todo1 =create_a_todo(title = 'testtitletodo1', headers = headers_user1)
    
    todo2 =create_a_todo(title = 'testtitletodo2', headers = headers_user1)
    
    client.delete(f'/todos/delete_todo/{todo1['id']}',headers = headers_user1)
    
    

    response = client.get(f"/admin/get_all_todos/{user_id}", headers=headers_admin)

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[1]['is_deleted'] == True
    assert response.json()[0]['is_deleted'] == False
        
    
    
#---------------------------------------------------------------------------------------------
def test_admin_get_other_user_single_todo_success(client,auth_header,create_user,create_a_todo,only_get_token):
    
    admin1_username = f"user_{uuid.uuid4().hex[:6]}"
    headers_admin = auth_header(username= admin1_username,password= 'admin1password',role = 'admin')
    
    user_username = f"user_{uuid.uuid4().hex[:6]}"
    user_password = 'randompass'
    role = 'user'
    user1 = create_user(username = user_username, password = user_password, role = role)
    user_id = user1['id']

    token_user = only_get_token(user_username, user_password)
    headers_user1 = {"Authorization" : f"Bearer {token_user}"}
    
    todo1 =create_a_todo(title = 'testtitletodo1', headers = headers_user1)
    todo1_id = todo1['id']
    todo2 =create_a_todo(title = 'testtitletodo2', headers = headers_user1)
    todo2_id = todo2['id']

    response1 = client.get(f"/admin/get_todo_by_id/{todo1_id}", headers=headers_admin)

    assert response1.status_code == 200
    assert response1.json()['title'] == 'testtitletodo1'
    
    response1 = client.get(f"/admin/get_todo_by_id/{todo2_id}", headers=headers_admin)

    assert response1.status_code == 200
    assert response1.json()['title'] == 'testtitletodo2'
    
def test_admin_get_other_user_single_todo_not_found_todo(client,auth_header,create_user,create_a_todo,only_get_token):
    
    admin1_username = f"user_{uuid.uuid4().hex[:6]}"
    headers_admin = auth_header(username= admin1_username,password= 'admin1password',role = 'admin')

    response = client.get(f"/admin/get_todo_by_id/{999999999}", headers=headers_admin)

    assert response.status_code == 404
    assert response.json()['detail'] == 'Todo not found'

def test_admin_get_other_user_single_todo_non_admin_user(client,auth_header,create_user,create_a_todo,only_get_token):
    
    user1_username = f"user_{uuid.uuid4().hex[:6]}"
    user1_password = 'randompass'
    role = 'user'
    user1 = create_user(username = user1_username, password = user1_password, role = role)
    user1_id = user1['id']
    
    token_user1 = only_get_token(user1_username, user1_password)
    headers_user1 = {"Authorization" : f"Bearer {token_user1}"}
    
    
    user2_username = f"user_{uuid.uuid4().hex[:6]}"
    user2_password = 'randompass'
    role = 'user'
    user2 = create_user(username = user2_username, password = user2_password, role = role)
    user2_id = user2['id']
    
    token_user2 = only_get_token(user2_username, user2_password)
    headers_user2 = {"Authorization" : f"Bearer {token_user2}"}
    
    todo1 =create_a_todo(title = 'testtitletodo1', headers = headers_user1)
    todo1_id = todo1['id']
    
    

    response = client.get(f"/admin/get_todo_by_id/{todo1_id}", headers=headers_user2)

    assert response.status_code == 403
    assert response.json()['detail'] == "Not authorized!"
  
#---------------------------------------------------------------------------------------------

def test_admin_update_todo_success(client, auth_header, create_user, create_a_todo, only_get_token):
    admin1_username = f"user_{uuid.uuid4().hex[:6]}"
    headers_admin = auth_header(username= admin1_username,password= 'admin1password',role = 'admin')
    
    user1_username = f"user_{uuid.uuid4().hex[:6]}"
    user1_password = 'randompass'
    role = 'user'
    user1 = create_user(username = user1_username, password = user1_password, role = role)
    user_id = user1['id']

    token_user1 = only_get_token(user1_username, user1_password)
    headers_user1 = {"Authorization" : f"Bearer {token_user1}"}
    
    todo1 =create_a_todo(title = 'testtitletodo1', headers = headers_user1)
    todo1_id = todo1['id']
    
    new_updated_todo = {
        "title": "updatedString",
        "description": "updateddescription",
        "status": "pending",
        "priority": "low",
        "due_date": "2026-05-06T13:33:46.721Z",
        "is_deleted": True,
    }
    response = client.put(f'/admin/update_todo/{todo1_id}', json= new_updated_todo, headers=headers_admin)
    
    assert response.status_code == 200
    assert response.json()['title'] == 'updatedString'
    assert response.json()['is_deleted'] == True
    
    
def test_admin_update_todo_not_found_todo(client, auth_header, create_user, create_a_todo, only_get_token):
    admin1_username = f"user_{uuid.uuid4().hex[:6]}"
    headers_admin = auth_header(username= admin1_username,password= 'admin1password',role = 'admin')
       
    new_updated_todo = {
        "title": "updatedString",
        "description": "updateddescription",
        "status": "pending",
        "priority": "low",
        "due_date": "2026-05-06T13:33:46.721Z",
        "is_deleted": True,
    }
    response = client.put(f'/admin/update_todo/{999999999}', json= new_updated_todo, headers=headers_admin)
    
    assert response.status_code == 404
    assert response.json()['detail'] == 'Todo not found'
    
    
def test_admin_update_todo_non_admin_user(client,auth_header,create_user,create_a_todo,only_get_token):
    
    user1_username = f"user_{uuid.uuid4().hex[:6]}"
    user1_password = 'randompass'
    role = 'user'
    user1 = create_user(username = user1_username, password = user1_password, role = role)
    user1_id = user1['id']
    
    token_user1 = only_get_token(user1_username, user1_password)
    headers_user1 = {"Authorization" : f"Bearer {token_user1}"}
    
    
    user2_username = f"user_{uuid.uuid4().hex[:6]}"
    user2_password = 'randompass'
    role = 'user'
    user2 = create_user(username = user2_username, password = user2_password, role = role)
    user2_id = user2['id']
    
    token_user2 = only_get_token(user2_username, user2_password)
    headers_user2 = {"Authorization" : f"Bearer {token_user2}"}
    
    todo1 =create_a_todo(title = 'testtitletodo1', headers = headers_user1)
    todo1_id = todo1['id']
    
    new_updated_todo = {
        "title": "updatedString",
        "description": "updateddescription",
        "status": "pending",
        "priority": "low",
        "due_date": "2026-05-06T13:33:46.721Z",
        "is_deleted": True,
    }
    response = client.put(f'/admin/update_todo/{todo1_id}', json= new_updated_todo, headers=headers_user2)
    
    assert response.status_code == 403
    assert response.json()['detail'] == "Not authorized!"
    
def test_admin_update_todo_failure_in_completed_todo(client, auth_header, create_user, create_a_todo, only_get_token):
    admin1_username = f"user_{uuid.uuid4().hex[:6]}"
    headers_admin = auth_header(username= admin1_username,password= 'admin1password',role = 'admin')
    
    user1_username = f"user_{uuid.uuid4().hex[:6]}"
    user1_password = 'randompass'
    role = 'user'
    user1 = create_user(username = user1_username, password = user1_password, role = role)
    user_id = user1['id']

    token_user1 = only_get_token(user1_username, user1_password)
    headers_user1 = {"Authorization" : f"Bearer {token_user1}"}
    
    todo1 =create_a_todo(title = 'testtitletodo1', headers = headers_user1)
    todo1_id = todo1['id']
    
    new_updated_todo = {
        "title": "updatedString",
        "description": "updateddescription",
        "status": "completed",
        "priority": "low",
        "due_date": "2026-05-06T13:33:46.721Z",
        "is_deleted": False,
    }
    response = client.put(f'/admin/update_todo/{todo1_id}', json= new_updated_todo, headers=headers_admin)
    
    assert response.status_code == 422
    

    
    
    
    
#---------------------------------------------------------------------------------------------
def test_admin_get_other_user_all_todos_with_owner_name_success(client,auth_header,create_user,create_a_todo,only_get_token):
    
    admin1_username = f"user_{uuid.uuid4().hex[:6]}"
    headers_admin = auth_header(username= admin1_username,password= 'admin1password',role = 'admin')
    
    user_username = f"user_{uuid.uuid4().hex[:6]}"
    user_password = 'randompass'
    role = 'user'
    user1 = create_user(username = user_username, password = user_password, role = role)
    user_id = user1['id']

    token_user = only_get_token(user_username, user_password)
    headers_user1 = {"Authorization" : f"Bearer {token_user}"}
    
    todo1 =create_a_todo(title = 'testtitletodo1', headers = headers_user1)
    todo2 =create_a_todo(title = 'testtitletodo2', headers = headers_user1)

    response = client.get(f"/admin/get_all_todos_with_owner/{user_id}", headers=headers_admin)

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]['owner']['username'] == user_username
    assert response.json()[1]['owner']['username'] == user_username
    
    
    
    
    
    
    
    