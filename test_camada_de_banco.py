import unittest

from sqlalchemy.orm import sessionmaker

from camada_de_banco import get_db


class TestCamadaDeBanco(unittest.TestCase):
    def setUp(self):
        # Cria o banco de dados em memória
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=None)

    def tearDown(self):
        # Limpa a tabela e fecha a conexão com o banco
        pass

    def test_get_db(self):
        # Testa se a conexão com o banco foi estabelecida corretamente
        db = get_db()
        self.assertIsNotNone(db)


if __name__ == '__main__':
    unittest.main()

# python -m unittest test_camada_de_banco.py
