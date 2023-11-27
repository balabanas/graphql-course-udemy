from graphene import Schema, ObjectType, String, Int, Field, List, Mutation


class UserType(ObjectType):
    id = Int()
    name = String()
    age = Int()


class CreateUser(Mutation):
    class Arguments:
        name = String()
        age = Int()

    user = Field(UserType)

    @staticmethod
    def mutate(root, info, name, age):
        new_user = {"id": len(Query.users) + 1, "name": name, "age": age}
        Query.users.append(new_user)
        return CreateUser(user=new_user)


class UpdateUser(Mutation):
    class Arguments:
        user_id = Int(required=True)
        name = String()
        age = Int()

    user = Field(UserType)

    @staticmethod
    def mutate(root, info, user_id, name=None, age=None):
        user = None
        for u in Query.users:
            if u["id"] == user_id:
                user = u
                break
        if not user:
            return None
        if name:
            user["name"] = name
        if age:
            user["age"] = age

        return UpdateUser(user=user)


class DeleteUser(Mutation):
    class Arguments:
        user_id = Int(required=True)
        name = String()
        age = Int()

    user = Field(UserType)

    @staticmethod
    def mutate(root, info, user_id):
        user = None
        for u in Query.users:
            if u["id"] == user_id:
                user = u
                Query.users.remove(u)
                break
        return DeleteUser(user=user)


class Query(ObjectType):
    user = Field(UserType, user_id=Int())
    users_by_min_age = List(UserType, min_age=Int())

    users = [
        {"id": 1, "name": "John", "age": 20},
        {"id": 2, "name": "Jane", "age": 22},
        {"id": 3, "name": "Bob", "age": 30},
        {"id": 4, "name": "Alice", "age": 25}
    ]

    @staticmethod
    def resolve_user(root, info, user_id):
        matched_users = [user for user in Query.users if user["id"] == user_id]
        return matched_users[0] if matched_users else None

    @staticmethod
    def resolve_users_by_min_age(root, info, min_age):
        return [user for user in Query.users if user["age"] >= min_age]


class Mutation(ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()


schema = Schema(query=Query, mutation=Mutation)

gql = '''
query {
    user(userId: 1) {
        id
        name
        age
    }
}
'''

# gql = '''
# query {
#     usersByMinAge(minAge: 21) {
#         id
#         name
#
#     }
# }
# '''

# gql = '''
# mutation {
#     createUser(name: "test", age: 20) {
#         user {
#             id
#             name
#             age
#         }
#     }
# }
# '''

gql_update = """
mutation {
    updateUser(userId: 1, age: 11) {
        user {
            id
            name
            age
        }
    }
}
"""

gql_delete = """
mutation {
    deleteUser(userId: 15) {
        user {
            id
            name
            age
        }
    }
}
"""

if __name__ == '__main__':
    print(schema.execute(gql))
    print(schema.execute(gql_delete))
    print(schema.execute(gql))
