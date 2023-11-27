from graphene import Mutation, Int, Field
from graphql import GraphQLError

from app.db.database import Session
from app.db.models import JobApplication
from app.gql.types import JobApplicationObject
from app.gql.user.mutation import logged_in_user_same_as


class AddJobApplication(Mutation):
    class Arguments:
        job_id = Int(required=True)
        user_id = Int(required=True)

    job_application = Field(lambda: JobApplicationObject)

    @logged_in_user_same_as
    @staticmethod
    def mutate(root, info, job_id, user_id):
        with Session() as session:
            job_application = session.query(JobApplication).where(JobApplication.job_id == job_id,
                                                                  JobApplication.user_id == user_id).first()
            if job_application:
                raise GraphQLError(f"Job application with job_id {job_id} and user_id {user_id} already exists")
            status = 'Applied'
            job_application = JobApplication(job_id=job_id, user_id=user_id, status=status)
            session.add(job_application)
            session.commit()
            session.refresh(job_application)
        return AddJobApplication(job_application=job_application)
