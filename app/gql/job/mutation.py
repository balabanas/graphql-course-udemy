from graphene import Mutation, String, Int, Field, Boolean

from app.db.database import Session
from app.db.models import Job
from app.gql.types import JobObject
from app.gql.user.mutation import admin_user


class AddJob(Mutation):
    class Arguments:
        title = String(required=True)
        description = String(required=True)
        employer_id = Int(required=True)

    job = Field(lambda: JobObject)

    @admin_user
    @staticmethod
    def mutate(root, info, title, description, employer_id):
        job = Job(title=title, description=description, employer_id=employer_id)
        with Session() as session:
            session.add(job)
            session.commit()
            session.refresh(job)
            return AddJob(job=job)


class UpdateJob(Mutation):
    class Arguments:
        id = Int(required=True)
        title = String()
        description = String()
        employer_id = Int()

    job = Field(lambda: JobObject)

    @admin_user
    @staticmethod
    def mutate(root, info, id, title=None, description=None, employer_id=None):
        with Session() as session:
            job = session.query(Job).where(Job.id == id).first()
            # job = session.query(Job)\
            #     .options(joinedload(Job.employer))\
            #     .where(Job.id == id).first()
            if not job:
                raise Exception(f"Job with id {id} not found")
            if title:
                job.title = title
            if description:
                job.description = description
            if employer_id:
                job.employer_id = employer_id
            session.commit()
            session.refresh(job)
            return UpdateJob(job=job)


class DeleteJob(Mutation):
    class Arguments:
        id = Int(required=True)

    job = Field(lambda: JobObject)
    success = Boolean()

    @admin_user
    @staticmethod
    def mutate(root, info, id):
        with Session() as session:
            job = session.query(Job).where(Job.id == id).first()
            if not job:
                raise Exception(f"Job with id {id} not found")
            session.delete(job)
            session.commit()
            return DeleteJob(job=job, success=True)
