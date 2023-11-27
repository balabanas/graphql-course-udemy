from fastapi import FastAPI
from graphene import Schema
from starlette_graphene3 import GraphQLApp, make_playground_handler

from app.db.database import prepare_database
from app.gql.mutation import Mutation
from app.gql.queries import Query

schema = Schema(query=Query, mutation=Mutation)

app = FastAPI()


@app.on_event("startup")
def startup_event():
    prepare_database()


app.mount("/", GraphQLApp(
    schema=schema,
    on_get=make_playground_handler())
          )
