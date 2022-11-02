from sqlalchemy import Column, Integer, Float, Text, Time, Sequence, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import BYTEA, ARRAY
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


class Coords(Base):
    __tablename__ = "coords"
    id = Column(Integer, Sequence("coords_id_seq"), primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    height = Column(Integer)


class PerevalImages(Base):
    __tablename__ = "pereval_images"
    id = Column(Integer, Sequence("pereval_images_id_seq"), primary_key=True)
    date_added = Column(Time)
    title = Column(Text)
    data = Column(BYTEA)


class PerevalAdded(Base):
    __tablename__ = "pereval_added"
    id = Column(Integer, Sequence("pereval_added_id_seq"), primary_key=True)
    add_time = Column(Time)
    beauty_title = Column(Text)
    title = Column(Text)
    other_titles = Column(Text)
    connect = Column(Text)
    user_id = Column(Integer, ForeignKey(User.id))
    coords_id = Column(Integer, ForeignKey(Coords.id))
    level_winter = Column(Text)
    level_summer = Column(Text)
    level_autumn = Column(Text)
    level_spring = Column(Text)
    images = Column(ARRAY(Integer))
    UniqueConstraint(user_id, coords_id)


Base.metadata.create_all(engine)


