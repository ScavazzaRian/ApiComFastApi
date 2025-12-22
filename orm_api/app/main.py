from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine, get_db
from app import models, schemas
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/produtos/create", response_model=schemas.ProdutoResponse, status_code=201)
def create(request: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    produto = models.Produto(**request.model_dump())

    db.add(produto)
    db.commit()
    db.refresh(produto)

    return produto

@app.get("/produtos", response_model=List[schemas.ProdutoResponse], status_code=200)
def read(db:Session = Depends(get_db)):
    produtos = db.query(models.Produto).all()
    return produtos

@app.delete("/produtos/{id}/delete", status_code=204)
def delete(id: int, db: Session = Depends(get_db)):
    query = db.query(models.Produto).filter(models.Produto.id == id)
    produto = query.first()

    if not produto:
        raise HTTPException(status_code=404, detail="Produto nao encontrado")
    
    query.delete(synchronize_session=False)
    db.commit()

    return None

@app.patch("/produtos/{id}/update", response_model=schemas.ProdutoResponse, status_code=201)
def update(id: int, request: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    query = db.query(models.Produto).filter(models.Produto.id == id)
    produto = query.first()

    if not produto:
        raise HTTPException(status_code=404, detail="Produto nao encontrado")

    dados_atualizados = request.model_dump(exclude_unset=True)

    query.update(dados_atualizados)
    db.commit()
    
    return query.first() 