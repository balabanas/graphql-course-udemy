import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.data import employers_data, jobs_data, users_data, job_applications_data
from app.db.models import Base, Employer, Job, User, JobApplication


load_dotenv()
print(os.getenv('DB_URL'))
engine = create_engine(os.getenv('DB_URL'), echo=True)
conn = engine.connect()

Session = sessionmaker(bind=engine)
session = Session()


def prepare_database():
    from app.utils import hash_password
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = Session()
    for employer in employers_data:
        session.add(Employer(**employer))
    for job in jobs_data:
        session.add(Job(**job))
    for user in users_data:
        user["password_hash"] = hash_password(user["password"])
        del user["password"]
        session.add(User(**user))
    session.commit()
    for job_application in job_applications_data:
        session.add(JobApplication(**job_application))
    session.commit()
    session.close()
