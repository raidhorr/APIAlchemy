from sqlalchemy import Column, Integer, Text, Sequence, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base

from sqlalch import engine

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    email = Column(Text)
    phone = Column(Text)
    fam = Column(Text)
    name = Column(Text)
    otc = Column(Text)
    UniqueConstraint(email)


Base.metadata.create_all(engine)


