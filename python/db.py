from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from os import getenv
from model import User


def make_session():
    dbuser = getenv("DB_USER")
    dbhost = getenv("DB_HOST")
    dbpass = getenv("DB_PASSWORD")
    dbname = getenv("DB_DATABASE")
    driver = "mysql+pymysql"
    engine = create_engine(f"{driver}://{dbuser}:{dbpass}@{dbhost}/{dbname}")
    return sessionmaker(bind=engine)


Session = make_session()


def get_userdata(username):
    query = select(User).where(User.username == username)

    with Session() as session:
        user_data = session.scalars(query).first() or User(
            username="", password="", salt="", role=""
        )

    return user_data
