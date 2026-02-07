from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

DATABASE_URL = "sqlite:///ecommerce.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Импортируем модели для регистрации в Base.metadata
from app.models import categories, products  # noqa


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
