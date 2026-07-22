async def test_signup_success(client, user_data):
    response = await client.post("/api/v1/users/signup", json=user_data)

    data = response.json()

    assert response.status_code == 201
    assert data["name"] == data["name"]
    assert data["lastname"] == data["lastname"]
    assert data["email"] == data["email"]
    assert data["is_admin"] == data["is_admin"]
    assert "password" not in data

async def test_signup_duplicate_email(client, user_data):
    await client.post("/api/v1/users/signup", json=user_data)

    response = await client.post("/api/v1/users/signup", json=user_data)

    assert response.status_code == 406

async def test_login_success(client, created_user):
    response = await client.post("/api/v1/users/login", data={
        "username": created_user["request"]["email"],
        "password": created_user["request"]["password"],
        },
    )

    data = response.json()

    assert response.status_code == 200
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    

async def test_login_wrong_password(client, created_user):
    response = await client.post("/api/v1/users/login", data={
        "username": created_user["request"]["email"],
        "password": "incorrect password",
        },
    )

    assert response.status_code == 400
    
