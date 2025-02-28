from django.urls import path
from . import views

urlpatterns = [
    path('', views.photo_list, name='photo_list'),
    path('upload/', views.photo_upload, name='photo_upload'),
    path('delete/<int:pk>/', views.photo_delete, name='photo_delete'),  # Маршрут для удаления
    path('photo/<int:pk>/', views.photo_detail, name='photo_detail'),  # Новый маршрут для деталей

    path('admin-list/', views.admin_list, name='admin_list'),
]
