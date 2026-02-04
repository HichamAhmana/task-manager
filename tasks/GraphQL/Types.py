import graphene
from graphene_django import DjangoObjectType
from ..models import Task


class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        # Only expose fields frontend needs
        fields = ("id", "title", "completed", "created_at", "updated_at")
