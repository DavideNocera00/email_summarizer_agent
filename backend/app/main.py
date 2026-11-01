from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

from starlette.middleware.sessions import SessionMiddleware

from app.config import settings
from app.auth import oauth
from app.crud import insert_user
from app.database import get_db
from app.models import User

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
async def callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    userinfo = token["userinfo"]

    user = insert_user(db, userinfo["email"], token.get("refresh_token"))
    request.session["user_id"] = user.id
    return RedirectResponse("/me")

@app.get("/me")
def me(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not Authenticated")

    user = db.get(User, user_id)
    return {"id": user.id, "email": user.email}