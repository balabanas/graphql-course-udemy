from graphene import ObjectType, List, Field, Int

from app.db.database import Session
from app.db.models import Job, Employer, User, JobApplication
from app.gql.types import JobObject, EmployerObject, UserObject, JobApplicationObject


class Query(ObjectType):
    job = Field(JobObject, id=Int(required=True))
    jobs = List(JobObject)
    employer = Field(EmployerObject, id=Int(required=True))
    employers = List(EmployerObject)
    user = Field(lambda: UserObject, id=Int(required=True))
    users = List(lambda: UserObject)
    job_application = Field(lambda: JobApplicationObject, id=Int(required=True))
    job_applications = List(lambda: JobApplicationObject)

    @staticmethod
    def resolve_job(root, info, id):
        return Session().query(Job).where(Job.id == id).first()

    @staticmethod
    def resolve_jobs(root, info):
        jobs = Session().query(Job).all()
        # Note: if we are to close Session (with the context manager, for example), the field-level resolvers will fail
        return jobs

    @staticmethod
    def resolve_employer(root, info, id):
        return Session().query(Employer).where(Employer.id == id).first()

    @staticmethod
    def resolve_employers(root, info):
        employers = Session().query(Employer).all()
        # Note: if we are to close Session (with the context manager, for example), the field-level resolvers will fail
        return employers

    @staticmethod
    def resolve_user(root, info, id):
        return Session().query(User).where(User.id == id).first()

    @staticmethod
    def resolve_users(root, info):
        users = Session().query(User).all()
        return users

    @staticmethod
    def resolve_job_application(root, info, id):
        return Session().query(JobApplication).where(JobApplication.id == id).first()

    @staticmethod
    def resolve_job_applications(root, info):
        job_applications = Session().query(JobApplication).all()
        return job_applications
