from django.contrib import admin

from todo.models import TodoItem, TodoList


admin.site.register(TodoItem)
admin.site.register(TodoList)
