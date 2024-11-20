from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker

from config import settings

url_object = URL.create(
    drivername="mysql+mysqldb",
    username=settings.MYSQL_USER,
    password=settings.MYSQL_PASSWORD,
    host=settings.MYSQL_HOST,
    port=settings.MYSQL_PORT,
    database=settings.MYSQL_DB,
)
engine = create_engine(url_object, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
