from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

class Produto(BaseModel):
    id: Optional[int] = None
    name: str
    price: float
    descricao: str

data = []
id_inicial = 1

@app.post("/create", response_model=Produto, status_code=status.HTTP_201_CREATED, tags=["Produtos"])
def create_product(produto: Produto):
    if not produto.name or not produto.descricao:
        raise HTTPException(status_code=400, detail="Nome e descricao nao podem ser vazios")
    elif produto.price <= 0:
        raise HTTPException(status_code=400, detail="O preco do produto deve ser maior que 0")
    else:
        global id_inicial
        produto.id = id_inicial

        data.append(produto)

        id_inicial += 1
        return produto

@app.get("/itens", response_model=list[Produto], status_code=status.HTTP_200_OK, tags=["Produtos"])
def read_products():
    return data

@app.delete("/itens/delete/{id}", response_model=Produto, status_code=status.HTTP_200_OK, tags=["Produtos"])
def delete_product(id: int):
    for produto in data:
        if produto.id == id:
            data.remove(produto)
            return produto
    
    raise HTTPException(status_code=404, detail="Produto Inexistente")
        
@app.put("/itens/update/{id}", response_model=Produto, status_code=status.HTTP_200_OK, tags=["Produtos"])
def update_product(id: int, produto_atualizado: Produto):
    for produto in data:
        if produto.id == id:
            if not produto_atualizado.name or not produto_atualizado.descricao:
                raise HTTPException(status_code=400, detail="Nome e descricao nao podem ser vazios")
            elif produto_atualizado.price <= 0:
                raise HTTPException(status_code=400, detail="O preco do produto deve ser maior que 0")
            else:
                produto.name = produto_atualizado.name
                produto.price = produto_atualizado.price
                produto.descricao = produto_atualizado.descricao

            return produto
        
    raise HTTPException(status_code=404, detail="Produto Inexistente")