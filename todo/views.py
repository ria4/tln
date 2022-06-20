from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views.generic.edit import ModelFormMixin

from todo.mixins import (
    TodoCurrentUserFilterMultipleObjectMixin,
    TodoCurrentUserFilterSingleObjectMixin,
    TodoGroupRequiredMixin,
)
from todo.models import TodoItem, TodoList


# Todo Lists

class TodoListListView(
    TodoGroupRequiredMixin,
    TodoCurrentUserFilterMultipleObjectMixin,
    ListView,
):
    model = TodoList
    template_name = 'todo/index.html'


class TodoListCreateView(
    TodoGroupRequiredMixin,
    TodoCurrentUserFilterSingleObjectMixin,
    CreateView,
):
    model = TodoList
    fields = ['title', 'public']

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = "Add a new list"
        return context

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

class TodoItemListView(AccessMixin, ListView):
    model = TodoItem
    template_name = 'todo/todo_list.html'

    def dispatch(self, request, *args, **kwargs):
        todo_list = get_object_or_404(TodoList, id=self.kwargs['list_id'])
        if not (todo_list.public or todo_list.author == request.user):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return TodoItem.objects.filter(todo_list_id=self.kwargs['list_id'])

    def get_context_data(self):
        context = super().get_context_data()
        context['todo_list'] = TodoList.objects.get(id=self.kwargs['list_id'])
        return context


class TodoItemCreateView(
    TodoGroupRequiredMixin,
    TodoCurrentUserFilterSingleObjectMixin,
    CreateView,
):
    model = TodoItem
    fields = ['todo_list', 'title']

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = "Add a new list"
        return context

    def get_initial(self):
        initial_data = super().get_initial()
        todo_list = TodoList.objects.get(id=self.kwargs['list_id'])
        initial_data['todo_list'] = todo_list
        return initial_data

    def get_context_data(self):
        context = super().get_context_data()
        todo_list = TodoList.objects.get(id=self.kwargs['list_id'])
        context['todo_list'] = todo_list
        context['title'] = "Create a new item"
        return context

    def get_success_url(self):
        return reverse('list', args=[self.object.todo_list_id])


class TodoItemUpdateView(
    TodoGroupRequiredMixin,
    TodoCurrentUserFilterSingleObjectMixin,
    UpdateView,
):
    model = TodoItem
    fields = ['todo_list', 'title']

    def get_context_data(self):
        context = super().get_context_data()
        todo_list = TodoList.objects.get(id=self.kwargs['list_id'])
        context['todo_list'] = todo_list
        context['title'] = "Edit item"
        return context

    def get_success_url(self):
        return reverse('list', args=[self.object.todo_list_id])


class TodoItemDeleteView(
    TodoGroupRequiredMixin,
    TodoCurrentUserFilterSingleObjectMixin,
    DeleteView,
):
    model = TodoItem

    def get_success_url(self):
        return reverse_lazy('list', args=[self.kwargs['list_id']])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo_list'] = self.object.todo_list
        return context
