from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse
from src.utils.OAuth import oauth  # Import the configured OAuth object

google_auth_router = APIRouter(tags=["GoogleAuth"])

@google_auth_router.get("/auth/google")
async def auth_google(request: Request):
    redirect_uri = request.url_for('auth_google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@google_auth_router.get("/auth/google/callback")
async def auth_google_callback(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = await oauth.google.parse_id_token(request, token)
    except Exception as e:
        return RedirectResponse(url='/')

    # Handle user creation or lookup here, generate JWT
    return {'user_info': user_info}