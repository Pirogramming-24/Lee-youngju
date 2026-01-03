from django.urls import path
from . import views

app_name = 'idea'

urlpatterns = [
    path('', views.idea_list, name='list'),
    path('register/', views.idea_register, name='register'),
    path('<int:idea_id>/', views.idea_detail, name='detail'),
    path('<int:idea_id>/update/', views.idea_update, name='update'),
    path('<int:idea_id>/delete/', views.idea_delete, name='delete'),
    path('<int:idea_id>/toggle_star/', views.toggle_star, name='toggle_star'),
    path('<int:idea_id>/adjust_interest/', views.adjust_interest, name='adjust_interest'),
]
