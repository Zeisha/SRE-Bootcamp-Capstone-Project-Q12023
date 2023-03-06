from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from os import getenv
from model import User

dbuser = getenv("DB_USER")
dbhost = getenv("DB_HOST")
dbpass = getenv("DB_PASSWORD")
dbname = getenv("DB_DATABASE")

# Create a database engine
engine = create_engine(f"mysql+pymysql://{dbuser}:{dbpass}@{dbhost}/{dbname}")
# Create a session object
Session = sessionmaker(bind=engine)


def get_userdata(username):
    query = select(User).where(User.username == username)

    with Session() as session:
        user_data = session.scalars(query).first() or User(
            username="", password="", salt="", role=""
        )

    return user_data
