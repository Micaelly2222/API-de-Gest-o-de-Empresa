import unittest

from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# classe base para os testes
Base = declarative_base()


# modelo para teste
class TestModel(Base):
    __tablename__ = "test_model"
    id = Column(Integer, primary_key=True)
    name = Column(String)


# classe de teste para a camada de banco
class TestCamadaDeBanco(unittest.TestCase):
    def setUp(self):
        # configuração do banco de dados de teste
        SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"
        engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)
        Base.metadata.create_all(bind=engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.engine = engine

    def tearDown(self):
        # limpeza após cada teste
        Base.metadata.drop_all(bind=self.engine)

    def test_insert_record(self):
        # teste básico de inserção de registro
        with self.get_db() as db:
            # cria um novo registro
            test_model = TestModel(name="Test")
            db.add(test_model)
            db.commit()

            # recupera o registro
            retrieved_model = db.query(TestModel).filter_by(name="Test").first()

            # verifica se o registro foi inserido corretamente
            self.assertIsNotNone(retrieved_model)
            self.assertEqual(retrieved_model.name, "Test")


if __name__ == "__main__":
    unittest.main()

# python -m unittest test_camada_de_banco.py
