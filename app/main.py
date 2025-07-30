from fastapi import FastAPI
from api.routers.crud import crud_router   
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()
app.include_router(crud_router)
register_tortoise(
    app=app,
    db_url="sqlite://crud.db",
    add_exception_handlers=True,
    generate_schemas=True,
    modules={"models": ["api.models.crud"]}
)

@app.get("/")
def index():
    return {"status": "todo api is running"}