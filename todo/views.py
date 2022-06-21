from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views.generic.edit import ModelFormMixin

from todo.mixins import (
    TodoCurrentUserFilterMultipleObjectMixin,
    TodoCurrentUserFilterSingleObjectMixin,
    TodoGroupRequiredMixin,
    TodoListFilterMixin,
)
from todo.models import TodoItem, TodoList


# Todo Lists

class TodoListListView(
    TodoGroupRequiredMixin,
    TodoCurrentUserFilterMultipleObjectMixin,
    ListView,
):
    model = TodoList
    template_name = 'todo/todolist_list.html'


class TodoListCreateView(
    TodoGroupRequiredMixin,
    TodoCurrentUserFilterSingleObjectMixin,
    CreateView,
):
    model = TodoList
    fields = ['title', 'public']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super(ModelFormMixin, self).form_valid(form)


class TodoListDeleteView(
    TodoGroupRequiredMixin,
    TodoCurrentUserFilterSingleObjectMixin,
    DeleteView,
):
    model = TodoList
    success_url = reverse_lazy('index')


# Todo Items

class TodoItemListView(
    TodoListFilterMixin,
    PermissionRequiredMixin,
    ListView,
):
    model = TodoItem
    template_name = 'todo/todoitem_list.html'

    def has_permission(self):
        todo_list = self.extra_context['todo_list']
        return todo_list.public or todo_list.author == self.request.user

    def get_queryset(self):
        return self.extra_context['todo_list'].items.all()


class TodoItemCreateView(
    TodoGroupRequiredMixin,
    TodoListFilterMixin,
    TodoCurrentUserFilterSingleObjectMixin,
    CreateView,
):
    model = TodoItem
    fields = ['content']

    def form_valid(self, form):
        form.instance.todo_list = self.extra_context['todo_list']
        return super().form_valid(form)

    def get_success_url(self):
        list_id = self.kwargs['list_id']
        return reverse('list', kwargs={'list_id': list_id})


class TodoItemUpdateView(
    TodoGroupRequiredMixin,
    TodoListFilterMixin,
    TodoCurrentUserFilterSingleObjectMixin,
    UpdateView,
):
    model = TodoItem
    fields = ['content']

    def form_valid(self, form):
        form.instance.todo_list = self.extra_context['todo_list']
        return super().form_valid(form)

    def get_success_url(self):
        list_id = self.kwargs['list_id']
        return reverse('list', kwargs={'list_id': list_id})


class TodoItemDeleteView(
    TodoGroupRequiredMixin,
    TodoListFilterMixin,
    TodoCurrentUserFilterSingleObjectMixin,
    DeleteView,
):
    model = TodoItem

    def get_success_url(self):
        return reverse_lazy('list', args=[self.kwargs['list_id']])
