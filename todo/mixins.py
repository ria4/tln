from abc import ABC

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from todo.constants import TODO_ACCESS_GROUP
from todo.models import TodoItem, TodoList


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
