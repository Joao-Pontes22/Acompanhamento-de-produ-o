from sqlalchemy.orm import sessionmaker
from Models.Models import engine

def Init_Session():
    Session = None
    try:
     Session = sessionmaker(bind=engine)
     session = Session()
     yield session
    finally:
     session.close()
     print("Session closed.")