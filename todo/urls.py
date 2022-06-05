from django.urls import path

from todo import views


urlpatterns = [
    path('', views.TodoListListView.as_view(), name='index'),
    path('list/<int:list_id>/', views.TodoItemListView.as_view(), name='list'),
    path('list/<int:pk>/delete/', views.TodoListDeleteView.as_view(), name='list-delete'),
    path('list/add/', views.TodoListCreateView.as_view(), name='list-add'),
    path('list/<int:list_id>/item/add/', views.TodoItemCreateView.as_view(), name='item-add'),
    path('list/<int:list_id>/item/<int:pk>', views.TodoItemUpdateView.as_view(), name='item-update'),
    path('list/<int:list_id>/item/<int:pk>/delete/', views.TodoItemDeleteView.as_view(), name='item-delete'),
]
