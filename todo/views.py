from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views.generic.edit import ModelFormMixin

from todo.mixins import ToDoGroupRequiredMixin
from todo.models import ToDoItem, ToDoList


# Todo Lists

class ToDoListListView(ToDoGroupRequiredMixin, ListView):
    model = ToDoList
    template_name = 'todo/index.html'


class ToDoListCreateView(ToDoGroupRequiredMixin, CreateView):
    model = ToDoList
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


class ToDoListDeleteView(ToDoGroupRequiredMixin, DeleteView):
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


class ToDoItemCreateView(ToDoGroupRequiredMixin, CreateView):
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


class ToDoItemUpdateView(ToDoGroupRequiredMixin, UpdateView):
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


class ToDoItemDeleteView(ToDoGroupRequiredMixin, DeleteView):
    model = ToDoItem

    def get_success_url(self):
        return reverse_lazy('list', args=[self.kwargs['list_id']])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo_list'] = self.object.todo_list
        return context
