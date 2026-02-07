from fastapi import FastAPI


from app.routers import categories
from app.routers import products
from app.database import Base, engine

app = FastAPI(
    title="FastAPI Интернет-магазин",
    version="0.1.0",
)




Base.metadata.create_all(bind=engine)


app.include_router(categories.router)
app.include_router(products.router)

@app.get("/")
async def root():

    return {"message": "Добро пожаловать в API Интернет-магазина!"}