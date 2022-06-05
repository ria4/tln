from django.contrib.auth.mixins import LoginRequiredMixin

from todo.constants import TODO_ACCESS_GROUP


class ToDoGroupRequiredMixin(LoginRequiredMixin):
    """Mixin which raises a 403 if the user is not part of the TODO group."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name=TODO_ACCESS_GROUP).exists():
            return super().handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
