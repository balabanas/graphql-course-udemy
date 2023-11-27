from graphene import ObjectType, Int, String, Field, List

from app.db.data import jobs_data, employers_data
from app.db.database import Session
from app.db.models import Job, Employer


class EmployerObject(ObjectType):
    id = Int()
    name = String()
    contact_email = String()
    industry = String()
    jobs = List(lambda: JobObject)

    @staticmethod
    def resolve_jobs(root, info):
        # with Session() as session:
        #     jobs = session.query(Job).where(Job.employer_id == root.id).all()
            # return jobs
        # return # [job for job in jobs_data if job["employer_id"] == root["id"]]
        return root.jobs


class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field(lambda: EmployerObject)
    job_applications = List(lambda: JobApplicationObject)

    @staticmethod
    def resolve_employer(root, info):
        # with Session() as session:
        #     employer = session.query(Employer).where(Employer.id == root.employer_id).first()
        #     return employer
        return root.employer

    @staticmethod
    def resolve_job_applications(root, info):
        return root.job_applications


class UserObject(ObjectType):
    id = Int()
    username = String()
    email = String()
    role = String()
    job_applications = List(lambda: JobApplicationObject)

    @staticmethod
    def resolve_job_applications(root, info):
        return root.job_applications

class JobApplicationObject(ObjectType):
    id = Int()
    job_id = Int()
    user_id = Int()
    status = String()
    job = Field(lambda: JobObject)
    user = Field(lambda: UserObject)
    message = String()

    @staticmethod
    def resolve_job(root, info):
        return root.job

    @staticmethod
    def resolve_user(root, info):
        return root.user
