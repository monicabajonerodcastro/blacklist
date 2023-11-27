from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

engine = create_engine(
   url= "postgresql://{}:{}@{}:{}/{}".format("postgres", "postgres", "blacklist.cojnzeopmjcz.us-east-1.rds.amazonaws.com", "5432", "postgres"),
)

db_session = scoped_session(
    sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False
    )
)

Base = declarative_base()