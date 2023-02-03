from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import BooleanField, ExpressionWrapper, Q
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


class TodoNowView(ListView):
    """Return a list of the admin's public TodoLists."""
    queryset = TodoList.objects.filter(author=1, public=True)
    template_name = 'todo/todolist_now.html'


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


class TodoListUpdateView(
    TodoGroupRequiredMixin,
    TodoListFilterMixin,
    TodoCurrentUserFilterSingleObjectMixin,
    UpdateView,
):
    model = TodoList
    fields = ['title', 'public']


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
        """Display items starting with '[long term]' first."""
        qs = self.extra_context['todo_list'].items.all()
        expression = Q(content__startswith="[long term]")
        is_longterm = ExpressionWrapper(expression, output_field=BooleanField())
        return qs.annotate(is_longterm=is_longterm).order_by("-is_longterm")


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
        return reverse('list', args=[self.kwargs['list_id']])


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
        return reverse('list', args=[self.kwargs['list_id']])


class TodoItemDeleteView(
    TodoGroupRequiredMixin,
    TodoListFilterMixin,
    TodoCurrentUserFilterSingleObjectMixin,
    DeleteView,
):
    model = TodoItem

    def get_success_url(self):
        return reverse('list', args=[self.kwargs['list_id']])
