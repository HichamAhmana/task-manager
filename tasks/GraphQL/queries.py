import graphene
from graphql import GraphQLError
from tasks.models import Task
from tasks.GraphQL.Types import TaskType

class TaskQuery(graphene.ObjectType):
    my_tasks = graphene.List(TaskType)

    def resolve_my_tasks(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("You must be logged in to view tasks")

        return Task.objects.filter(owner=user)
