from django.db import models

from todo.utils import generate_key


class Base(models.Model):
    """Abstract base model. Includes columns that should be included on
    all application models."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(Base):
    """Application authentication model."""

    username = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.username


class Key(Base):
    """API key model, used to authenticate API requests to users."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # In a production setting, we'd want to store a hash of the key, not the raw
    # key string.
    key = models.CharField(unique=True, max_length=255, default=generate_key)

    class Meta:
        default_related_name = "keys"


class TodoList(Base):
    """Todo list model."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        default_related_name = "lists"

    def __str__(self):
        return self.name


class TodoTask(Base):
    """Todo list task model."""

    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    task = models.TextField()
    due_at = models.DateTimeField(null=True)
    completed_at = models.DateTimeField(null=True)

    class Meta:
        default_related_name = "tasks"
