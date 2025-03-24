from fastapi import APIRouter, Depends, Cookie, HTTPException, Request
from database import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth
from datetime import datetime, timedelta
from jose import jwt, ExpiredSignatureError, JWTError
import uuid
from model import GoogleToken, GoogleUser, RoleTable
from fastapi.responses import RedirectResponse
import httpx
import os 
from dotenv import load_dotenv


load_dotenv()




db_dpendencies = Annotated[Session, Depends(get_db)]

# router = APIRouter(
#     prefix="/auth",
#     tags=["Auth"]
# )

router = APIRouter()


###############################################################################


# oauth = OAuth()
# oauth.register(
#     name="auth_demo",
#     client_id=config("GOOGLE_CLIENT_ID"),
#     client_secret=config("GOOGLE_CLIENT_SECRET"),
#     authorize_url="https://accounts.google.com/o/oauth2/auth",
#     authorize_params=None,
#     access_token_url="https://accounts.google.com/o/oauth2/token",
#     access_token_params=None,
#     refresh_token_url=None,
#     authorize_state=config("SECRET_KEY"),
#     redirect_uri="http://127.0.0.1:8000/auth",
#     jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
#     client_kwargs={"scope": "openid profile email"},
# )


####################################################################################


Alogrithm = "HS256"
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SCREAT = os.getenv("GOOGLE_CLIENT_SCREAT")
SECRET_KEY = os.getenv("SECRET_KEY")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
REDIRECT_URL = "http://127.0.0.1:8000/auth"
FRONTEND_URL = "http://127.0.0.1:8000/docs"

oauth = OAuth()

oauth.register(
    name="Test",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SCREAT,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params=None,
    access_token_url="https://accounts.google.com/o/oauth2/token",
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri="http://127.0.0.1:8000/auth",
    jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
    client_kwargs={"scope": "openid profile email"},

)

def create_access_token(data: dict, expire_delta: timedelta):

    to_encode = data.copy()

    expire = datetime.utcnow() + (expire_delta or timedelta(minutes=30))
    
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, Alogrithm)


def get_current_user(request: Request):
    
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authorized") 
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[Alogrithm])
        user_id = payload.get("sub")
        email = payload.get("email")

        return {"user_id": user_id, "email": email}
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=404, detail="JWT token has been expired")
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")
    

def validate_user_request(token: str = Cookie(None)):

    session_detail = get_current_user(token)

    return session_detail

# @router.get("/login")
# async def login(request: Request):

#     request.session.clear()
#     referer = request.headers.get("referer")
#     frontend_url = None
#     redirect_url = REDIRECT_URL
#     request.session["login_redirect"] = frontend_url 

#     return await oauth.auth_demo.authorize_redirect(request, redirect_url, prompt="consent")
    

@router.get("/login")
async def login(request: Request):

    request.session.clear()  #this wil clear the previous user or yoiurs login session
    referer = request.headers.get("referer")  #this will get the url of front end from where you started to redirated back 
    frontend_url = "http://127.0.0.1:8000/docs"  
    redirect_url = REDIRECT_URL
    request.session["login_redirect"] = frontend_url  # this is to save the frontend url so that later we can sent user to from where they came

    return await oauth.Test.authorize_redirect(request, redirect_url, prompt="consent")  #this first redirect user to the google login and then redirect back from where they started


@router.get("/auth")
async def auth(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.Test.authorize_access_token(request)
        user_info = token.get("userinfo")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unverified")

    if not user_info:
        raise HTTPException(status_code=401, detail="Google authentication failed")

    expires_in = token.get("expires_in")
    user_id = user_info.get("sub")
    iss = user_info.get("iss")
    user_email = user_info.get("email")
    username = user_info.get("name") or user_email.split("@")[0]
    user_pic = user_info.get("picture")
    first_logged_in = datetime.utcnow()
    last_accessed = datetime.utcnow()

    if iss not in ["https://accounts.google.com", "accounts.google.com"]:
        raise HTTPException(status_code=401, detail="Google authentication failed")

    if not user_id:
        raise HTTPException(status_code=401, detail="Google authentication failed")

    token_expire = timedelta(seconds=expires_in)
    access_token = create_access_token(data={"sub": user_id, "email": user_email, "role": "user"}, expire_delta=token_expire)

    session_id = str(uuid.uuid4())
    log_user(user_id, username, user_email, user_pic, first_logged_in, last_accessed, db)
    log_token(access_token, user_email, session_id, db)
    role(user_email, db)

    redirect_url = request.session.pop("login_redirect", FRONTEND_URL)
    response = RedirectResponse(url=redirect_url)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        domain="127.0.0.1",  # Match your domain
        path="/"  # Available on all paths
    )
    return response





def log_user(user_id, username, user_email, user_pic, first_logged_in, last_accessed, db: Session):

    google_user = GoogleUser(
        user_id=user_id,
        username=username,
        user_email=user_email,
        user_pic=user_pic,
        first_logged_in=first_logged_in,
        last_accessed=last_accessed
    )

    db.add(google_user)
    
    db.commit()



def log_token(access_token, user_email, session_id, db: Session):

    google_token = GoogleToken(
        access_token=access_token,
        user_email=user_email,
        session_id=session_id
    )

    db.add(google_token)
    db.commit()

def role(email, db: Session):

    role = RoleTable(
        email=email,
        role="user"
    )

    db.add(role)
    db.commit()




@router.get("/logout")
async def logout(request: Request):
    request.session.clear()

    response = RedirectResponse(url="/")

    response.delete_cookie("access_token")

    return response

    
    
    
    






