from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

DATABASE = {
    'drivername': 'postgresql+psycopg2',
    'host': os.getenv('FSTR_DB_HOST'),
    'port': os.getenv('FSTR_DB_PORT'),
    'username': os.getenv('FSTR_DB_LOGIN'),
    'password': os.getenv('FSTR_DB_PASS'),
    'database': 'postgres'
}

engine = create_engine(URL(**DATABASE), echo=True)
Session = sessionmaker(bind=engine)
session = Session()


