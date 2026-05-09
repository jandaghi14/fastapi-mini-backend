import uuid
# =================================================================================  
def test_register_user(client):
    response = client.post(
        '/register', 
        json={
            "username": "user1test",
            "password" : "user1password",
            "role" : "user"})
    assert response.status_code == 200
    assert 'user1test' in response.json()['username']
#================================== 
def test_register_existing_user(client):
    client.post(
        '/register', 
        json={
            "username": "user1test",
            "password" : "user1password",
            "role" : "user"})
    response = client.post(
        '/register', 
        json={
            "username": "user1test",
            "password" : "user1password",
            "role" : "user"})
    assert response.status_code == 409
# =================================================================================  
def test_login_user(client, create_user):
    response = client.post('/login', data={
            "username": "user1test",
            "password" : "user1password"})
    assert response.status_code == 200        
    assert "Bearer" in response.json()['token_type']
#==================================
def test_login_wronge_user(client, create_user):
    response = client.post('/login', data={
            "username": "user2test",
            "password" : "user1password"})
    assert response.status_code == 401    
    assert response.json()['detail'] == "Either Username or Password is wrong !"    
# =================================================================================  

def test_endpoint_me(client, auth_header):

    username = f"user_{uuid.uuid4().hex[:6]}"
    response =  client.get('/me', headers= auth_header(username,'randompassword', 'user'))
    assert response.status_code == 200
    assert response.json()['username'] == username
    

