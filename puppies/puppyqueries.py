from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from puppies import Base, Shelter, Puppy

engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bin = engine

DBsession = sessionmaker(bind=engine)

session = DBsession()

def get_all_puppies():
    results = session.query(Puppy.name).all()
    for puppy in results:
        print(puppy[0])

if __name__ == '__main__':
    get_all_puppies()





