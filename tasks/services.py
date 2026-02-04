from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from .models import Task
from django.shortcuts import get_object_or_404


def get_user_tasks(user: User):
    """
    Return all tasks belonging to the given user.
    """
    if not user.is_authenticated:
        raise PermissionDenied("You must be logged in")

    return Task.objects.filter(owner=user)


def create_task(user: User, title: str):
    """
    Create a new task for the given user.
    """
    if not user.is_authenticated:
        raise PermissionDenied("You must be logged in")

    return Task.objects.create(
        title=title,
        owner=user
    )


def update_task(user: User, task_id: int, title=None, completed=None):
    """
    Update a task if the user owns it.
    """
    if not user.is_authenticated:
        raise PermissionDenied("You must be logged in")

    task = get_object_or_404(Task, id=task_id)

    if task.owner != user:
        raise PermissionDenied("Not allowed")

    if title is not None:
        task.title = title

    if completed is not None:
        task.completed = completed

    task.save()
    return task


def delete_task(user: User, task_id: int):
    """
    Delete a task if the user owns it.
    """
    if not user.is_authenticated:
        raise PermissionDenied("You must be logged in")

    task = get_object_or_404(Task, id=task_id)


    if task.owner != user:
        raise PermissionDenied("Not allowed")

    task.delete()
    return True
