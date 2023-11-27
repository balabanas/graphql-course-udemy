from graphene import ObjectType

from app.gql.employer.mutation import AddEmployer, UpdateEmployer, DeleteEmployer
from app.gql.job.mutation import AddJob, UpdateJob, DeleteJob
from app.gql.job_application.mutation import AddJobApplication
from app.gql.user.mutation import LoginUser, AddUser


class Mutation(ObjectType):
    add_job = AddJob.Field()
    update_job = UpdateJob.Field()
    delete_job = DeleteJob.Field()
    add_employer = AddEmployer.Field()
    update_employer = UpdateEmployer.Field()
    delete_employer = DeleteEmployer.Field()
    login_user = LoginUser.Field()
    add_user = AddUser.Field()
    add_job_application = AddJobApplication.Field()
