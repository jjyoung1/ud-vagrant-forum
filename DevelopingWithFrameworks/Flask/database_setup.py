import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        return {
            'name' : self.name,
            'id' : self.id
        }

class MenuItem(Base):
    __tablename__ = 'menu_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        return {
            'name' : self.name,
            'description' : self.description,
            'price' : self.price,
            'course' : self.course,
            'id' : self.id,
            'restaurant_id' : self.restaurant_id
        }

# Create engine for specified database
engine = create_engine('sqlite:///restaurantmenu.db')

# Bind the engine to the declarative_base
# Base.metadata.bind = engine

Base.metadata.create_all(engine)

# Create factory for making Session objects
# DBSession = sessionmaker(bind = engine)

####### Example Code ########
# newEntry = ClassName(property = "value", ...)
# session = DBSession()
# session.add(newEntry)
# session.commit()

