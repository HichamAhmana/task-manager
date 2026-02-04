import graphene
from graphene import ObjectType, Field, List, ID
from .Types import TaskType
from ..services import get_user_tasks
from django.core.exceptions import PermissionDenied


class TaskQuery(ObjectType):
    my_tasks = List(TaskType)
    task = Field(TaskType, id=ID(required=True))

    def resolve_my_tasks(root, info):
        user = info.context.user
        return get_user_tasks(user)

    def resolve_task(root, info, id):
        user = info.context.user
        tasks = get_user_tasks(user)
        try:
            return tasks.get(id=id)
        except tasks.model.DoesNotExist:
            raise PermissionDenied("Task not found or access denied")
