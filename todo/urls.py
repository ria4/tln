from django.urls import path

from todo import views


urlpatterns = [
    path('', views.TodoListListView.as_view(), name='index'),
    path('lists/', views.TodoListListView.as_view()),
    path('lists/<int:list_id>/', views.TodoItemListView.as_view(), name='list'),
    path('lists/<int:pk>/delete/', views.TodoListDeleteView.as_view(), name='list-delete'),
    path('lists/add/', views.TodoListCreateView.as_view(), name='list-add'),
    path('lists/<int:list_id>/items/add/', views.TodoItemCreateView.as_view(), name='item-add'),
    path('lists/<int:list_id>/items/<int:pk>', views.TodoItemUpdateView.as_view(), name='item-update'),
    path('lists/<int:list_id>/items/<int:pk>/delete/', views.TodoItemDeleteView.as_view(), name='item-delete'),
]
