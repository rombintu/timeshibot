from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
# TODO
class User(Base):
    __tablename__ = "Groups"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
