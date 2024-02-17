from django.db import models

from todo.utils import generate_key


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(Base):
    username = models.CharField(unique=True, max_length=255)


class Key(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(unique=True, max_length=255, default=generate_key)

    class Meta:
        default_related_name = "keys"


class TodoList(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        default_related_name = "lists"


class TodoTask(Base):
    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    task = models.TextField()
    due_at = models.DateTimeField(null=True)
    completed_at = models.DateTimeField(null=True)

    class Meta:
        default_related_name = "tasks"
