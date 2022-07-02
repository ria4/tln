from abc import ABC

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.views.generic.base import ContextMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from todo.constants import TODO_ACCESS_GROUP
from todo.models import TodoItem, TodoList


class TodoListFilterMixin(ContextMixin, View):
    """Check for the list_id validity and add it to the context data."""

    def dispatch(self, request, *args, **kwargs):
        self.extra_context = self.extra_context or {}
        if 'list_id' in self.kwargs:
            todo_list = get_object_or_404(TodoList, id=self.kwargs['list_id'])
        else:
            todo_list = get_object_or_404(TodoList, id=self.kwargs['pk'])
        self.extra_context.update(todo_list=todo_list)
        return super().dispatch(request, *args, **kwargs)


class TodoGroupRequiredMixin(LoginRequiredMixin):
    """Raise a 403 if the user is not part of the TODO group."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name=TODO_ACCESS_GROUP).exists():
            return super().handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class TodoCurrentUserObjectMixin(ABC):
    """Filter queryset according to the current user.

    Works for both TodoList & TodoItem models."""

    def get_queryset(self):
        qs = super().get_queryset()
        if qs.model == TodoList:
            kwargs = {'author': self.request.user}
        elif qs.model == TodoItem:
            kwargs = {'todo_list__author': self.request.user}
        return qs.filter(**kwargs)


class TodoCurrentUserFilterSingleObjectMixin(
    TodoCurrentUserObjectMixin,
    SingleObjectMixin,
):
    pass


class TodoCurrentUserFilterMultipleObjectMixin(
    TodoCurrentUserObjectMixin,
    MultipleObjectMixin,
):
    pass
