from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()  # Cargar variables de entorno desde el archivo .env

DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_USER = os.getenv('DB_USER')
DB_DIALECT = os.getenv('DB_DIALECT')

URL_CONECTION = '{}://{}:{}@{}/{}'.format(DB_DIALECT, DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

engine = create_engine(URL_CONECTION)

#bind es la forma de conexión a la base de datos
#autocommit es para que no se haga commit automáticamente
#autoflush es para que no se haga flush automáticamente
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()