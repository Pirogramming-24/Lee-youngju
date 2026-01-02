from django.urls import path
from . import views

app_name = 'tool'

urlpatterns = [
    path('', views.tool_list, name='list'),
    path('register/', views.tool_register, name='register'),
    path('<int:tool_id>/', views.tool_detail, name='detail'),
    path('<int:tool_id>/update/', views.tool_update, name='update'),
    path('<int:tool_id>/delete/', views.tool_delete, name='delete'),
]
