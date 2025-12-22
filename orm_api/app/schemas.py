from pydantic import BaseModel
from typing import Optional

class ProdutoBase(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoResponse(ProdutoBase):
    id: int

    # Basicamente o SQLAlchemy retorna um objeto, porem o pydantic precisa dessa classe para ler as prorpiedades como Json usando o obj.prop
    class Config:
        from_attributes = True