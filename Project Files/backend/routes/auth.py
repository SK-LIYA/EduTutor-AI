from fastapi import Request, APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth
import requests
import os

config = Config('.env')

oauth = OAuth(config)
oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'}
)

auth_router = APIRouter(prefix="/auth", tags=["Google Auth"])

@auth_router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for('auth_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@auth_router.get("/callback")
async def auth_callback(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)

        user_info_response = requests.get(
            'https://www.googleapis.com/oauth2/v3/userinfo',
            headers={'Authorization': f'Bearer {token["access_token"]}'}
        )

        user_info = user_info_response.json()

        request.session['user'] = dict(user_info)
        request.session['token'] = token

        return RedirectResponse(url="/docs")

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Google authentication failed: {str(e)}")
