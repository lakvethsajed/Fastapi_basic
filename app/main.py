from fastapi import FastAPI
from . import models
from .database import engine ,SessionLocal
from . import config
from .routers import books, users,auth,issues
from fastapi.middleware.cors import CORSMiddleware
models.Base.metadata.create_all(bind=engine)


app = FastAPI() 
origins= ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)
app.include_router(books.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(issues.router)
@app.get("/")
def message():
    return {"message": "Welcome to Library"}

