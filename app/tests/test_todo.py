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
        user = auth_header('usertest','randompass','user')
        response = client.post('/todos/create_todo', json={
            'title' : 'qw',
            'description' : 'description',
            'priority' : 'low'},
             headers= user       )
        assert response.status_code == 422


