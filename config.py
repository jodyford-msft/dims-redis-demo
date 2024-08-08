import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging 
class Config:
    # SQL Server connection parameters
    SERVER = 'vectorblacknet-server.database.windows.net'
    DATABASE = 'VectorBlack'
    USER = 'vectorblacknet-server-admin'
    PASSWORD = ''  # Replace with actual password
    DRIVER = 'ODBC Driver 17 for SQL Server'
    REDIS_URL = os.getenv('REDIS_URL', 'redis://:')
    REDIS_HOST = ''
    REDIS_PORT = 6380
    REDIS_PASSWORD = ''
    REDIS_SSL = True
    
    # SQLAlchemy Database URI using SQL Server login
    SQLALCHEMY_DATABASE_URI = (
        f"mssql+pyodbc://{USER}:{PASSWORD}@{SERVER}:1433/{DATABASE}?driver={DRIVER}"
    )
    logging.error(SQLALCHEMY_DATABASE_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Initialize Redis client
 
    
    # Redis URL (example)
    REDIS_URL = os.getenv('REDIS_URL', '')

    def get_engine_kwargs(self):
        return {
            "connect_args": {
                "Encrypt": "yes",
                "TrustServerCertificate": "no",
                "Connection Timeout": 30
            }
        }

# Create SQLAlchemy engine
def create_db_engine():
    config = Config()
    engine = create_engine(
        config.SQLALCHEMY_DATABASE_URI,
        **config.get_engine_kwargs()
    )
    return engine

# Create a new SQLAlchemy session
def create_db_session():
    engine = create_db_engine()
    Session = sessionmaker(bind=engine)
    return Session()
