from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from todo.constants import TODO_ACCESS_GROUP


class TodoGroupRequiredMixin(LoginRequiredMixin):
    """Raise a 403 if the user is not part of the TODO group."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name=TODO_ACCESS_GROUP).exists():
            return super().handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class TodoListCurrentUserFilterSingleObjectMixin(SingleObjectMixin):
    """Filter queryset according to the current user."""

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author=self.request.user)


class TodoListCurrentUserFilterMultipleObjectMixin(MultipleObjectMixin):
    """Filter queryset according to the current user."""

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author=self.request.user)


class TodoItemCurrentUserFilterSingleObjectMixin(SingleObjectMixin):
    """Filter queryset according to the current user."""

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(todo_list__author=self.request.user)
