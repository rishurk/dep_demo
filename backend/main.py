from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import engine, sessionLocal, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins="http://localhost:63342",
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/about")
def hello():
    return {'message' : "bond mra"}

@app.post("/users")
def create_user(user: schemas.userCreate, db: Session = Depends(get_db)):
    new_user = models.User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created", "user": {"id": new_user.id, "name": new_user.name, "email": new_user.email}}
