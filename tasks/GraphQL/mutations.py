# tasks/graphql/mutations.py
import graphene
from graphql import GraphQLError
from tasks.GraphQL.Types import TaskType
from tasks import services

from django.contrib.auth.models import User
from tasks.services import register_user, login_user
from tasks.GraphQL.Types import UserType  # We'll create this type next
# -------------------
# CREATE TASK
# -------------------
class CreateTask(graphene.Mutation):
    task = graphene.Field(TaskType)

    class Arguments:
        title = graphene.String(required=True)

    def mutate(self, info, title):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("You must be logged in to create tasks")

        task = services.create_task(user, title)
        return CreateTask(task=task)


# -------------------
# UPDATE TASK
# -------------------
class UpdateTask(graphene.Mutation):
    task = graphene.Field(TaskType)

    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        completed = graphene.Boolean()

    def mutate(self, info, id, title=None, completed=None):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("You must be logged in to update tasks")

        task = services.update_task(user, id, title, completed)
        return UpdateTask(task=task)


# -------------------
# DELETE TASK
# -------------------
class DeleteTask(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("You must be logged in to delete tasks")

        services.delete_task(user, id)
        return DeleteTask(success=True)


# -------------------
# AGGREGATED MUTATIONS
# -------------------
class TaskMutation(graphene.ObjectType):
    createTask = CreateTask.Field()
    updateTask = UpdateTask.Field()
    deleteTask = DeleteTask.Field()



# -------------------
# REGISTER MUTATION
# -------------------
class RegisterUser(graphene.Mutation):
    user = graphene.Field(lambda: UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        try:
            user = register_user(username, password)
        except Exception as e:
            raise GraphQLError(str(e))
        return RegisterUser(user=user)


# -------------------
# LOGIN MUTATION
# -------------------
class LoginUser(graphene.Mutation):
    user = graphene.Field(lambda: UserType)
    token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        try:
            user, token = login_user(username, password)
        except Exception as e:
            raise GraphQLError(str(e))
        return LoginUser(user=user, token=token)


# -------------------
# AGGREGATED USER MUTATIONS
# -------------------
class UserMutation(graphene.ObjectType):
    registerUser = RegisterUser.Field()
    loginUser = LoginUser.Field()