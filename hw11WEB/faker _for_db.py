from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from faker import Faker
from passlib.context import CryptContext

fake = Faker()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    birthday = Column(Date)
    additional_info = Column(String, nullable=True)


engine = create_engine('postgresql://postgres:vfrc3224@localhost/fastapi_db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def create_user(email: str, password: str):
    hashed_password = pwd_context.hash(password)
    user = User(email=email, hashed_password=hashed_password)
    session.add(user)
    session.commit()
    return user


def create_contact(user_id):
    return Contact(
        user_id=user_id,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        phone_number=fake.phone_number(),
        birthday=fake.date_of_birth(),
        additional_info=fake.text() if fake.boolean(chance_of_getting_true=50) else None
    )


user1 = create_user("user1@example.com", "password1")
user2 = create_user("user2@example.com", "password2")


for _ in range(5):
    contact1 = create_contact(user_id=user1.id)
    session.add(contact1)
    contact2 = create_contact(user_id=user2.id)
    session.add(contact2)

session.commit()

session.close()
