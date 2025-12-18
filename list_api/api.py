from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Estudo de FastApi",
    description="""Api para gestao de produtos
    
    Funcionalidades:

    - Listagem de produtos
    - Criacao de produtos
    - Atualizacao de produtos
    - Remocao de produtos
    """
)

class Produto(BaseModel):
    id: Optional[int] = Field(None, description="Primary key")
    name: str = Field(..., example="Cadeira Gamer", description="Nome completo do item")
    price: float = Field(..., example="23.90", description="Preço unitário em Reais")
    descricao: str = Field(..., example="Cadeira Gamer Kabum GMR", description="Especificacoes tecnicas")

data = []
id_inicial = 1

@app.post("/create", response_model=Produto, status_code=status.HTTP_201_CREATED, tags=["Produtos"])
def create_product(produto: Produto):
    """
        Cria um novo produto.

        - **name** : Passe uma string valida
        - **price**: Passe um valor de venda maior que 0
        - **descricao**: Passe uma string valida

        - **Retorno**: Retorna **201** caso o recurso seja criado, ou **400** caso alguns dos requisitos nao tenha sido atingido
    """
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
    """
        Devolve ao usuario a lista completa de produtos cadastrados.
    """
    return data

@app.delete("/itens/delete/{id}", response_model=Produto, status_code=status.HTTP_200_OK, tags=["Produtos"])
def delete_product(id: int):
    """
    Exclui um produto.
    
    - **id**: Passe o ID numérico do produto que deseja deletar.
    - **Retorno**: Confirmação da exclusao ou erro 404 caso não exista.
    """
    for produto in data:
        if produto.id == id:
            data.remove(produto)
            return produto
    
    raise HTTPException(status_code=404, detail="Produto Inexistente")
        
@app.put("/itens/update/{id}", response_model=Produto, status_code=status.HTTP_200_OK, tags=["Produtos"])
def update_product(id: int, produto_atualizado: Produto):
    """
    Atualiza um produto existente um produto.
    
    - **id**: Passe o ID numérico do produto que deseja deletar.
    - **Retorno**: Retorna o produto atualizado ou erro **404** caso não exista ou **400** caso alguns dos requisitos nao tenha sido atingido.
    """
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