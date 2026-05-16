import uuid



def test_pagination_user(client, create_user, create_a_todo, auth_header):
    headers = auth_header('test1user' , 'randompassword', 'user')
    
    create_a_todo(headers = headers )
    create_a_todo(headers = headers )
    create_a_todo(headers = headers )
    create_a_todo(headers = headers )
    create_a_todo(headers = headers )

    response = client.get('/todos/get_all_todos', 
                          headers= headers
                          )
    assert response.status_code == 200
    assert len(response.json()) == 5
    
    response = client.get('/todos/get_all_todos', 
                          params= {'limit' : 3,
                                  'offset' : 1},
                          headers= headers
                          )
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_pagination_admin(client, create_a_todo, auth_header, only_get_token, create_user):
    admin_headers = auth_header('usertestadmin' , 'randompasswordadmin', 'admin')
    
    username = uuid.uuid4().hex[:6]
    user = create_user(username , 'randompassword', 'user')
    
    token = only_get_token(username , 'randompassword')
    user_headers  = {"Authorization" : f"Bearer {token}"}
    user_id = user['id']
    
    
    
    create_a_todo(headers = user_headers )
    create_a_todo(headers = user_headers )
    create_a_todo(headers = user_headers )
    create_a_todo(headers = user_headers )
    create_a_todo(headers = user_headers )

    response = client.get(f'/admin/get_all_todos/{user_id}', 
                          headers= admin_headers,
                          
                          )
    assert response.status_code == 200
    assert len(response.json()) == 5
    
    response = client.get(f'/admin/get_all_todos/{user_id}', 
                          params= {'limit' : 3,
                                  'offset' : 1},
                          headers= admin_headers
                          )
    assert response.status_code == 200
    assert len(response.json()) == 3

def test_create_todo_title_too_short(client, auth_header):
        user = auth_header('usertest1','randompass','user')
        response = client.post('/todos/create_todo', json={
            'title' : 'qw',
            'description' : 'description',
            'priority' : 'low'},
             headers= user       )
        assert response.status_code == 422


def test_get_all_todos_with_owner(client, auth_header,create_a_todo):
    header = auth_header('test1username','randompass','user')
    create_a_todo(headers = header)
    response = client.get('/todos/get_all_todo_with_username', headers=header)
    assert response.status_code == 200
    assert response.json()[0]['owner']['username'] == 'test1username'
    

def test_updated_at_changes_on_update(auth_header, create_a_todo,client,create_user,only_get_token):
    import time
    
    
    username = uuid.uuid4().hex[:6]
    user = create_user(username , 'randompassword', 'user')
    
    token = only_get_token(username , 'randompassword')
    user_headers  = {"Authorization" : f"Bearer {token}"}
    user_id = user['id']
    
    
    
    
    
    todo =create_a_todo(headers = user_headers)
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
    
    
    response = client.put(f'/todos/update_todo/{todo_id}', headers=user_headers,  json= new_updated_todo)

    assert response.status_code == 200
    assert response.json()['updated_at'] != original_updated_at 

    
    