from flask_login import current_user

def test_login(client):
    with client:
        client.post("/login", data={"username": "user", "password": "wrongpassword"})
        assert current_user.is_authenticated == False

        client.post("/login", data={"username": "user", "password": "123123123"})
        assert current_user.is_authenticated