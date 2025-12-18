from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Produto(BaseModel):
    id: Optional[int] = None
    name: str
    price: float
    descricao: str

data = []
id_inicial = 1

@app.post("/create", response_model=Produto)
def create_product(produto: Produto):
    global id_inicial
    produto.id = id_inicial

    data.append(produto)

    id_inicial += 1
    return produto

@app.get("/itens", response_model=list[Produto])
def read_products():
    return data

@app.delete("/itens/delete/{id}", response_model=Produto)
def delete_product(id: int):
    for produto in data:
        if produto.id == id:
            data.remove(produto)
            return produto
        
@app.put("/itens/update/{id}", response_model=Produto)
def update_product(id: int, produto_atualizado: Produto):
    for produto in data:
        if produto.id == id:
            produto.name = produto_atualizado.name
            produto.price = produto_atualizado.price
            produto.descricao = produto_atualizado.descricao

            return produto