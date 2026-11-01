from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from app.config import settings
from app.auth import oauth

app = FastAPI(title="Email Summarizer Agent")
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.session_secret,
    https_only=False,
    same_site="lax"
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/auth/login")
async def login(request: Request):
    return await oauth.google.authorize_redirect(
        request,
        settings.google_redirect_uri,
        access_type="offline",
        prompt="consent",
    )

@app.get("/auth/callback")
async def callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    userinfo = token["userinfo"]
    return {
        "email": userinfo["email"],
        "has_refresh_token": "refresh_token" in token,
        "scope": token.get("scope"),
    }