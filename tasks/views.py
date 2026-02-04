from django.http import HttpResponse
from .models import Task

def task_home(request):
    tasks = Task.objects.all()

    response = ""
    for task in tasks:
        response += f"- {task.title}<br>"

    return HttpResponse(response)
