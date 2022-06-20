from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class TodoList(models.Model):
    title = models.CharField(max_length=100)
    public = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('list', args=[self.id])

    def __str__(self):
        return self.title


class TodoItem(models.Model):
    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse(
            'item-update', args=[str(self.todo_list.id), str(self.id)]
        )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created_at']
