import graphene
from .Types import TaskType
from tasks.models import Task
from ..services import create_task, update_task, delete_task
from django.core.exceptions import PermissionDenied
from tasks.GraphQL.Types import TaskType
from graphql import GraphQLError

class CreateTask(graphene.Mutation):
    task = graphene.Field(TaskType)

    class Arguments:
        title = graphene.String(required=True)

    def mutate(self, info, title):
        user = info.context.user
        task = create_task(user, title)
        return CreateTask(task=task)


class UpdateTask(graphene.Mutation):
    task = graphene.Field(TaskType)

    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        completed = graphene.Boolean()

    def mutate(self, info, id, title=None, completed=None):
        user = info.context.user
        task = update_task(user, id, title, completed)
        return UpdateTask(task=task)


class DeleteTask(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        user = info.context.user
        ok = delete_task(user, id)
        return DeleteTask(ok=ok)
    
class UpdateTaskCompleted(graphene.Mutation):
    class Arguments:
        task_id = graphene.ID(required=True)
        completed = graphene.Boolean(required=True)

    task = graphene.Field(TaskType)

    def mutate(self, info, task_id, completed):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Not logged in!")

        try:
            task = Task.objects.get(id=task_id, owner=user)
        except Task.DoesNotExist:
            raise GraphQLError("Task not found or not yours")

        task.completed = completed
        task.save()
        return UpdateTaskCompleted(task=task)

class TaskMutation(graphene.ObjectType):
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()
    delete_task = DeleteTask.Field()
    updateTaskCompleted = UpdateTaskCompleted.Field()
