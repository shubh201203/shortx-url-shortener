import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_shorten_url():
    """Verify that shortening a URL works and returns expected JSON context."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/shorten", json={"url": "https://google.com"})
    
    assert response.status_code == 200
    data = response.json()
    assert "short_code" in data
    assert data["original_url"] == "https://google.com"
    assert "status" in data

@pytest.mark.asyncio
async def test_redirect_cache_miss():
    """Verify that a DB miss successfully raises a 404 Not Found error."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/r/invalid_code_trigger_404")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_rate_limit_trigger():
    """Blast an endpoint to verify Redis sliding window returns 429 Too Many Requests."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        for _ in range(105):
            res = await ac.get("/r/rate_limit_test")
            if res.status_code == 429:
                break
        
        final_res = await ac.get("/r/rate_limit_test")
        assert final_res.status_code == 429

@pytest.mark.asyncio
async def test_redirect_success():
    """Verify standard redirect successfully routes after shortening a URL."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/shorten", json={"url": "https://example.com/target"})
        data = response.json()
        short_code = data["short_code"]
        
        # Test Redirect
        redirect_res = await ac.get(f"/r/{short_code}", follow_redirects=False)
        assert redirect_res.status_code in [307, 308, 302, 301]
        assert redirect_res.headers["location"] == "https://example.com/target"
