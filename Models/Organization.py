from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class Organization(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()), alias='_id',
                              description="Identificador da mensagem")
    name: str
    resume: Optional[str] = None
    url: Optional[str] = None
    address: Optional[str] = None
    contacts: Optional[list[str]] = Field(default_factory=list)
