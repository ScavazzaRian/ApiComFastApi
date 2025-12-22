from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import engine, get_db
from app import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/produtos/create", response_model=schemas.ProdutoResponse)
def create(request: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    produto = models.Produto(**request.model_dump())

    db.add(produto)
    db.commit()
    db.refresh(produto)

    return produto