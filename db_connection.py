from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class City(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)


engine = create_engine('sqlite:///weather.sqlite', echo=True, connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def add_city_to_db(name):
    query = session.query(City)
    identifier = query.count()
    city = City(id=identifier, name=name)
    session.add(city)
    session.commit()


def is_city_in_db(name):
    query = session.query(City)
    return query.filter(City.name == name).count() > 0


def all_cities():
    query = session.query(City)
    return query.all()


#query = session.query(City)
#query.delete()
#session.commit()
