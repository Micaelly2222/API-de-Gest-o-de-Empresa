from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String

from camada_de_banco import Base


class Organization(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()), alias='_id',
                              description="Identificador da mensagem")
    name: str
    resume: Optional[str] = None
    url: Optional[str] = None
    address: Optional[str] = None
    contacts: Optional[list[str]] = Field(default_factory=list)


class OrganizationEntity(Base):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    resume = Column(String)
    url = Column(String)
    address = Column(String)
    contacts = Column(String)
