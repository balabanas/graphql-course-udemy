from graphene import Mutation, String, Field, Int, Boolean

from app.db.database import Session
from app.db.models import Employer
from app.gql.types import EmployerObject
from app.gql.user.mutation import admin_user


class AddEmployer(Mutation):
    class Arguments:
        name = String(required=True)
        contact_email = String(required=True)
        industry = String(required=True)

    employer = Field(lambda: EmployerObject)

    # temp
    authenticated_as = Field(String)

    @admin_user
    @staticmethod
    def mutate(root, info, name, contact_email, industry):

        with Session() as session:
            employer = Employer(name=name, contact_email=contact_email, industry=industry)
            session.add(employer)
            session.commit()
            session.refresh(employer)
            return AddEmployer(employer=employer)


class UpdateEmployer(Mutation):
    class Arguments:
        id = Int(required=True)
        name = String()
        contact_email = String()
        industry = String()

    employer = Field(lambda: EmployerObject)

    @admin_user
    @staticmethod
    def mutate(root, info, id, name=None, contact_email=None, industry=None):
        with Session() as session:
            employer = session.query(Employer).where(Employer.id == id).first()
            if not employer:
                raise Exception(f"Employer with id {id} not found")
            if name:
                employer.name = name
            if contact_email:
                employer.contact_email = contact_email
            if industry:
                employer.industry = industry
            session.commit()
            session.refresh(employer)
            return UpdateEmployer(employer=employer)


class DeleteEmployer(Mutation):
    class Arguments:
        id = Int(required=True)

    employer = Field(lambda: EmployerObject)
    success = Boolean()

    @admin_user
    @staticmethod
    def mutate(root, info, id):
        with Session() as session:
            employer = session.query(Employer).where(Employer.id == id).first()
            if not employer:
                raise Exception(f"Employer with id {id} not found")
            session.delete(employer)
            session.commit()
            return DeleteEmployer(employer=employer, success=True)
