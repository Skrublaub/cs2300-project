from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = 'postgresql+psycopg2://root@172.69.0.4:5432/root' #needs port? Also no password after root:, may cause problems

engine = create_engine(URL_DATABASE, connect_args={'connect_timeout': 5})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
