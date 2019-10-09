from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()


class Puppy(Base):
    __tablename__ = 'puppy'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))

    # Add add a decorator property to serialize data from the database
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id
        }


class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key=True)
    restaurant_name = Column(String)
    restaurant_address = Column(String)
    restaurant_image = Column(String)

    # Add a property decorator to serialize information from this database
    @property
    def serialize(self):
        return {
            'restaurant_name': self.restaurant_name,
            'restaurant_address': self.restaurant_address,
            'restaurant_image': self.restaurant_image,
            'id': self.id

        }


engine = create_engine('sqlite:///puppies.db')
Base.metadata.create_all(engine)
