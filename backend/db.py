from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects.postgresql import ARRAY

# 🔥 IMPORTANT: replace with your real password
DATABASE_URL = "postgresql://postgres:1407@localhost:5432/agent_memory"

# Create engine
engine = create_engine(DATABASE_URL)

# Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base
Base = declarative_base()


# 🧠 Memory Table with Vector Embedding
class Memory(Base):
    __tablename__ = "memory"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text)
    response = Column(Text)

    # 🔥 Vector storage (embedding)
    embedding = Column(ARRAY(Text))


# 🔧 Initialize DB (creates table)
def init_db():
    Base.metadata.create_all(bind=engine)