from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
import json
from datetime import datetime

Base = declarative_base()


def get_database_connect():
    connect = json.load(open('settings.json'))
    return connect["database_connect"]


class Author(Base):
    __tablename__ = 'author'
    __table_args__ = {'schema': 'galery'}
    id = Column(String(36), primary_key=True)
    name = Column(String(400))

    def __init__(self, *args, **kwargs):
        super(Author, self).__init__(*args, **kwargs)


class Picture(Base):
    __tablename__ = 'picture'
    __table_args__ = {'schema': 'galery'}
    id = Column(String(36), primary_key=True)
    name = Column(String(400))
    description = Column(String(4000))
    author_id = Column(String(36), ForeignKey('galery.author.id'))
    size = Column(String(100))
    type = Column(String(100))
    url = Column(String(400), nullable=False)
    create_date = Column(DateTime, nullable=False)
    update_date = Column(DateTime, default=None)

    def __init__(self, *args, **kwargs):
        super(Picture, self).__init__(*args, **kwargs)
        self.create_date = datetime.now()


if __name__ == "__main__":
    engine = create_engine(get_database_connect(), echo=True)
    Base.metadata.create_all(engine)