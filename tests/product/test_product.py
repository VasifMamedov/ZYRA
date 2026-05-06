
def test_add_product_unauthorized(client):
    response = client.get("/create_product", follow_redirects=True)
    assert response.request.path == "/login"


def test_edit_product_unauthorized(client):
    response = client.get("/edit_product/1", follow_redirects=True)
    assert response.request.path == "/login"

def test_delete_product_unauthorized(client):
    response = client.get("/delete_product/1", follow_redirects=True)
    assert response.request.path == "/login"

def test_create_product(client):
    with client:
        client.post("/login", data = {"username" : "admin", "password": "123123123"})

        response = client.get("/create_product", follow_redirects=True)
        assert b"Product Name" in response.data