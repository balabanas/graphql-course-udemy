import os
from datetime import datetime, timedelta, timezone

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from dotenv import load_dotenv
from graphql import GraphQLError

from app.db.database import Session
from app.db.models import User


load_dotenv()


def generate_token(email: str) -> str:
    expiration_time = datetime.utcnow() + timedelta(minutes=int(os.getenv('TOKEN_EXPIRATION_TIME_MINUTES')))
    payload = {
        "email": email,
        "exp": expiration_time
    }
    token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm=os.getenv('ALGORITHM'))
    return token


def hash_password(pwd: str) -> str:
    ph = PasswordHasher()
    return ph.hash(pwd)


def verify_password(pwd_hash: str, pwd: str) -> [None | GraphQLError]:
    ph = PasswordHasher()
    try:
        ph.verify(pwd_hash, pwd)
    except VerifyMismatchError:
        raise GraphQLError("Invalid password")


def get_authenticated_user(context):
    request_object = context.get("request")
    auth_header = request_object.headers.get("Authentication")
    token = None
    if auth_header:
        token = auth_header.split(" ")
    if auth_header and len(token) == 2 and token[0] == "Bearer":
        try:
            payload = jwt.decode(token[1], os.getenv('SECRET_KEY'), algorithms=[os.getenv('ALGORITHM')])
            if datetime.now(timezone.utc) > datetime.fromtimestamp(payload["exp"], timezone.utc):
                raise GraphQLError("Token expired")
            session = Session()
            user = session.query(User).where(User.email == payload["email"]).first()
            return user
        except jwt.PyJWTError:
            raise GraphQLError("Invalid token")
    else:
        raise GraphQLError("Missing authentication token")
