from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=None)


def get_db():
    db = SessionLocal()
    try:
        return db
    except:
        db.close()
