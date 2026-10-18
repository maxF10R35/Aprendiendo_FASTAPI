from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
from database import LocalSession, engine
from schemas import UserData, UserId
from models import Base
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)
app = FastAPI()

origin = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = LocalSession()
    try:
        yield db   #yield es una llamada para abrir una sesión de base de datos y luego cerrarla después de que se complete la operación
    finally:
        db.close()


#Ruta Base 
@app.get("/")
def root():
    return 'Hi my name is FastApi 234234'


@app.get("/app/users/", response_model=list[UserId])
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db=db)


@app.get("/app/users/{id:int}", response_model=UserId)
def get_user(id: int, db: Session = Depends(get_db)):
    user_by_id = crud.get_user_by_id(db=db, id=id)
    if user_by_id:
        return user_by_id
    raise HTTPException(status_code=404, detail="No Encontrado el usuario")


@app.post("/app/users/", response_model=UserId)
def create_user(user: UserData, db: Session = Depends(get_db)):
    user_by_name = crud.get_user_by_name(db=db, name=user.name)
    if user_by_name:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    return crud.create_user(db=db, user=user)