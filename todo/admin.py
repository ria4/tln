from django.contrib import admin

from todo.models import ToDoItem, ToDoList


admin.site.register(ToDoItem)
admin.site.register(ToDoList)
