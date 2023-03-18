from typing import Optional

from pydantic import BaseModel, Field


class Organization(BaseModel):
    """Modelo de empresas"""
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()), alias='_id',
                              description="Identificador da mensagem")  # Optional: não é um campo obrigatorio
    name: str
    resume: Optional[str] = None
    url: Optional[str] = None
    address: Optional[str] = None
    contacts: Optional[list[str]] = Field(default_factory=list)
