from fastapi import FastAPI
from .routes import (
    authRoute,
    categoryRoute,
    chapterRoute,
    comicRoute,
    commentRoute,
    favoriteRoute,
    pageRoute,
    userRoute,
)

app = FastAPI()

app.include_router(authRoute.router)
app.include_router(userRoute.router)
app.include_router(comicRoute.router)
app.include_router(chapterRoute.router)
app.include_router(pageRoute.router)
app.include_router(categoryRoute.router)
app.include_router(favoriteRoute.router)
app.include_router(commentRoute.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
