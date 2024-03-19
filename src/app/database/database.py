import models.models as models
from sqlmodel import SQLModel, create_engine, Session
from config import DB_URL


engine = create_engine(DB_URL, echo=True)


def init_db():
    global engine

    print("Initialize database models")
    SQLModel.metadata.create_all(engine)
    print("Finish Initializing database models")


def get_session():
    with Session(engine) as session:
        yield session
