from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('create/', views.create_comment, name='create'),
    path('<int:comment_id>/update/', views.update_comment, name='update'),
    path('<int:comment_id>/delete/', views.delete_comment, name='delete'),
]