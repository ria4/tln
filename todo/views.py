from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from todo.models import ToDoItem, ToDoList


# Todo Lists

class ToDoListListView(LoginRequiredMixin, ListView):
    model = ToDoList
    template_name = 'todo/index.html'


class ToDoListCreateView(LoginRequiredMixin, CreateView):
    model = ToDoList
    fields = ['title']

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = "Add a new list"
        return context


class ToDoListDeleteView(LoginRequiredMixin, DeleteView):
    model = ToDoList
    success_url = reverse_lazy('index')


# Todo Items

class ToDoItemListView(ListView):
    model = ToDoItem
    template_name = 'todo/todo_list.html'

    def get_queryset(self):
        return ToDoItem.objects.filter(todo_list_id=self.kwargs['list_id'])

    def get_context_data(self):
        context = super().get_context_data()
        context['todo_list'] = ToDoList.objects.get(id=self.kwargs['list_id'])
        return context


class ToDoItemCreateView(LoginRequiredMixin, CreateView):
    model = ToDoItem
    fields = ['todo_list', 'title', 'description']

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = "Add a new list"
        return context

    def get_initial(self):
        initial_data = super().get_initial()
        todo_list = ToDoList.objects.get(id=self.kwargs['list_id'])
        initial_data['todo_list'] = todo_list
        return initial_data

    def get_context_data(self):
        context = super().get_context_data()
        todo_list = ToDoList.objects.get(id=self.kwargs['list_id'])
        context['todo_list'] = todo_list
        context['title'] = "Create a new item"
        return context

    def get_success_url(self):
        return reverse('list', args=[self.object.todo_list_id])


class ToDoItemUpdateView(LoginRequiredMixin, UpdateView):
    model = ToDoItem
    fields = ['todo_list', 'title', 'description']

    def get_context_data(self):
        context = super().get_context_data()
        todo_list = ToDoList.objects.get(id=self.kwargs['list_id'])
        context['todo_list'] = todo_list
        context['title'] = "Edit item"
        return context

    def get_success_url(self):
        return reverse('list', args=[self.object.todo_list_id])


class ToDoItemDeleteView(LoginRequiredMixin, DeleteView):
    model = ToDoItem

    def get_success_url(self):
        return reverse_lazy('list', args=[self.kwargs['list_id']])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo_list'] = self.object.todo_list
        return context
