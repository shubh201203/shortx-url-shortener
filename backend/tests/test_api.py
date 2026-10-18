import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture
def transport():
    return ASGITransport(app=app)

@pytest.mark.asyncio
async def test_options_cors_canonical_origin(transport):
    """Verify that OPTIONS preflight from the canonical production Vercel origin succeeds with CORS headers."""
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.options(
            "/api/shorten",
            headers={
                "Origin": "https://shortx-url-shortener.vercel.app",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type"
            }
        )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "https://shortx-url-shortener.vercel.app"
    assert "POST" in response.headers.get("access-control-allow-methods", "")

@pytest.mark.asyncio
async def test_options_cors_preview_origin(transport):
    """Verify that OPTIONS preflight from the exact user Vercel Preview origin succeeds."""
    preview_origin = "https://shortx-url-shortener-erd4ffgd1-shubh201203s-projects.vercel.app"
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.options(
            "/api/shorten",
            headers={
                "Origin": preview_origin,
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type"
            }
        )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == preview_origin
    assert "POST" in response.headers.get("access-control-allow-methods", "")

@pytest.mark.asyncio
async def test_options_disallowed_origin(transport):
    """Verify that an unauthorized origin is rejected with HTTP 400."""
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.options(
            "/api/shorten",
            headers={
                "Origin": "https://malicious-site.com",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type"
            }
        )
    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers

@pytest.mark.asyncio
async def test_options_other_project_preview_rejected(transport):
    """Verify that another user/project Vercel domain is rejected."""
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.options(
            "/api/shorten",
            headers={
                "Origin": "https://other-project-erd4ffgd1-otheruser.vercel.app",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type"
            }
        )
    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers

@pytest.mark.asyncio
async def test_health_check(transport):
    """Verify backend /health check returns 200 ok."""
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_validation_error_invalid_url(transport):
    """Verify invalid URL payloads receive 422 Unprocessable Entity."""
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/shorten", json={"url": "not-a-valid-url"})
    assert response.status_code == 422
