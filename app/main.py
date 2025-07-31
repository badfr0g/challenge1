from fastapi import FastAPI
from api.routers.restfulAPI import crud_router   
from tortoise.contrib.fastapi import register_tortoise
from strawberry.fastapi import GraphQLRouter
from api.routers.graphQL import schema

app = FastAPI()
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
app.include_router(crud_router, prefix="/api")
register_tortoise(
    app=app,
    db_url="sqlite://crud.db",
    add_exception_handlers=True,
    generate_schemas=True,
    modules={"models": ["api.models.crud"]}
)

@app.get("/")
def index():
    return {"status": "resfulAPI api is running"}
