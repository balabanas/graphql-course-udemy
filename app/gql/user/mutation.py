from functools import wraps

from graphene import String, Mutation, Field
from graphql import GraphQLError

from app.db.database import Session
from app.db.models import User
from app.gql.types import UserObject
from app.utils import generate_token, verify_password, hash_password, get_authenticated_user


class LoginUser(Mutation):
    class Arguments:
        email = String(required=True)
        password = String(required=True)

    token = String()

    @staticmethod
    def mutate(root, info, email, password):
        session = Session()
        user = session.query(User).where(User.email == email).first()
        if not user:
            raise GraphQLError("User not found")

        verify_password(pwd_hash=user.password_hash, pwd=password)

        # token = ''.join(choices(string.ascii_lowercase, k=18))
        token = generate_token(user.email)
        return LoginUser(token=token)


def admin_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1]
        user = get_authenticated_user(info.context)
        if user.role != "admin":
            raise GraphQLError("You are not authorized to perform this action")
        return func(*args, **kwargs)
    return wrapper


def logged_in_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1]
        user = get_authenticated_user(info.context)
        if not user:
            raise GraphQLError("You need to be logged in to perform this action")
        return func(*args, **kwargs)
    return wrapper


def logged_in_user_same_as(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1]
        user = get_authenticated_user(info.context)
        if user.id != kwargs['user_id']:
            raise GraphQLError(f"Authenticated user {user.id} is not authorized perform an action on behalf of {kwargs['user_id']}")
        return func(*args, **kwargs)
    return wrapper


class AddUser(Mutation):
    class Arguments:
        username = String(required=True)
        email = String(required=True)
        password = String(required=True)
        role = String(required=True)

    user = Field(lambda: UserObject)


    @admin_user
    @staticmethod
    def mutate(root, info, email, password, username, role):
        session = Session()
        user = session.query(User).where(User.email == email).first()
        if user:
            raise GraphQLError("User already exists")

        user = User(email=email, password_hash=hash_password(password), username=username, role=role)
        session.add(user)
        session.commit()
        session.refresh(user)

        token = generate_token(user.email)
        return AddUser(user=user)
