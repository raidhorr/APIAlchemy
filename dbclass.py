from sqlalchemy import Column, Integer, Float, Text, Time, Sequence, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import BYTEA, ARRAY
from sqlalchemy.orm import declarative_base
from json import loads, dumps
from datetime import datetime

from sqlalch import engine, session

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

    def submitData(self, data):
        try:
            pydata = loads(data)
            email = pydata['user']['email']
            user = session.query(User).filter(User.email == email)
            if user:
                user_id = user[0].id
            else:
                user = User(
                    email=email,
                    fam=pydata['user']['fam'],
                    name=pydata['user']['name'],
                    otc=pydata['user']['otc'],
                    phone=pydata['user']['phone'],
                )
                session.add(user)
                session.commit()
                user_id = user.id
            latitude = float(pydata['coords']['latitude'])
            longitude = float(pydata['coords']['longitude'])
            height = int(pydata['coords']['height'])
            coords = session.query(Coords).filter(
                Coords.latitude == latitude and
                Coords.longitude == longitude and
                Coords.height == height
            )
            if coords:
                coords_id = coords[0].id
            else:
                coords = Coords(
                    latitude=latitude,
                    longitude=longitude,
                    height=height
                )
                session.add(coords)
                session.commit()
                coords_id = coords.id
            date_added = datetime.strptime(pydata['add_time'], '%Y-%m-%d %H:%M:%S')
            image_list = []
            for rec in pydata['images']:
                image = PerevalImages(
                    date_added=date_added,
                    title=rec['title'],
                    data=rec['data']
                )
                session.add(image)
                session.commmit()
                image_list.append(image.id)

            pereval = PerevalAdded(
                add_time=date_added,
                beauty_title=pydata['beauty_title'],
                title=pydata['title'],
                other_titles=pydata['other_titles'],
                connect=pydata['connect'],
                user_id=user_id,
                coords_id=coords_id,
                level_winter=pydata['level']['winter'],
                level_summer=pydata['level']['summer'],
                level_autumn=pydata['level']['autumn'],
                level_spring=pydata['level']['spring'],
                images=image_list
            )
            session.add(pereval)
            session.commit()
            res = {
                'status': '200',
                'message': None,
                'id': pereval.id
            }
            return dumps(res)
        except KeyError as exp:
            res = {
                'status': '400',
                'message': exp,
                'id': None
            }
            return dumps(res)
        except Exception as exp:
            res = {
                'status': '500',
                'message': exp,
                'id': None
            }
            return dumps(res)


Base.metadata.create_all(engine)


