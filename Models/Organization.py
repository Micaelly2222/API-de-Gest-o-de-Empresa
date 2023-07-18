from sqlalchemy import Column, String

from camada_de_banco import Base


class Organization(Base):
    __tablename__ = 'organization'

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    resume = Column(String)
    url = Column(String)
    address = Column(String)
    contacts = Column(String)
