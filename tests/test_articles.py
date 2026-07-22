async def test_create_article(client, auth_token):
    response = await client.post("/api/v1/articles/", json={
            "title": "An article",
            "description": "Just an article",
            "source_url": "https://www.udemy.com/course/fastapi-apis-modernas-e-assincronas-com-python/learn/lecture/32054384#overview",
        },
        headers={
            "Authorization": f"Bearer {auth_token}",
        },
    )

    data = response.json()

    assert response.status_code == 201
    assert data["title"] == "An article"
    assert data["description"] == "Just an article"
    assert data["source_url"] == "https://www.udemy.com/course/fastapi-apis-modernas-e-assincronas-com-python/learn/lecture/32054384#overview"

async def test_get_article(client, created_article):
    response = await client.get("/api/v1/articles/")

    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1

async def test_get_article_by_id(client, created_article):
    response = await client.get(f"/api/v1/articles/{created_article['id']}")

    data = response.json()

    assert response.status_code == 200
    assert data["id"] == created_article["id"]

async def test_get_article_not_found(client):
    response = await client.get("/api/v1/articles/999")

    assert response.status_code == 404

async def test_update_article_without_token(client, created_article):
    response = await client.put(f"/api/v1/articles/{created_article['id']}", json={
        "title":  "Another Article",
	    "description": "Just an article",
	    "source_url": "https://www.udemy.com/course/fastapi-apis-modernas-e-assincronas-com-python/learn/lecture/32054384#overview"
    })
    assert response.status_code == 401

async def test_update_article_with_token(client, auth_token, created_article):
    response = await client.put(f"/api/v1/articles/{created_article['id']}", json={
        "title":  "Another Article",
	    "description": "Just an article",
	    "source_url": "https://www.udemy.com/course/fastapi-apis-modernas-e-assincronas-com-python/learn/lecture/32054384#overview"
    }, headers={"Authorization": f"Bearer {auth_token}"})

    data = response.json()

    assert response.status_code == 202
    assert data["title"] == "Another Article"
    assert data["description"] == "Just an article"
    assert data["source_url"] == "https://www.udemy.com/course/fastapi-apis-modernas-e-assincronas-com-python/learn/lecture/32054384#overview"

async def test_delete_article(client, auth_token, created_article):
    response = await client.delete(f"/api/v1/articles/{created_article['id']}", 
                                   headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 204
    
