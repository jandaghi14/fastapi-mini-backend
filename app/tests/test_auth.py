def test_jwt_flow(client):
    client.post(
        '/register', 
        json={
            "username": "usertestjwt",
            "password" : "user1password",
            "role" : "user"})
    
    login_response = client.post('/login', data={
            "username": "usertestjwt",
            "password" : "user1password"})
    
    token = login_response.json()['access_token']

    response = client.get('/me', headers={
        "Authorization" : f"Bearer {token}"
    })
    
    assert response.status_code == 200
    assert response.json()['username'] == "usertestjwt"
    
#========================================================    
def test_jwt_flow_wrong_token(client):
    client.post(
        '/register', 
        json={
            "username": "usertest",
            "password" : "user1password",
            "role" : "user"})
    
    login_response = client.post('/login', data={
            "username": "usertest",
            "password" : "user1password"})
    
    token = login_response.json()['access_token']

    response = client.get('/me', headers={
        "Authorization" : f"Bearers {token}"
    })
    
    assert response.status_code == 401
    assert response.json()['detail'] == "Not authenticated" 
#========================================================    
def test_jwt_flow_expired_token(client):
    from app.core.authentication import create_access_token
    from datetime import timedelta
    from app.core.enums import UserRole
    client.post(
        '/register', 
        json={
            "username": "usertest",
            "password" : "user1password",
            "role" : "user"})
    
    expired_token = create_access_token('usertest', 1, UserRole.user,delta_expire=timedelta(seconds=-10))

    response = client.get('/me', headers={
        "Authorization" : f"Bearer {expired_token}"
    })
    
    assert response.status_code == 401
    assert response.json()['detail'] == "Authentication failed!" 
#========================================================    



