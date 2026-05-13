from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('incident/new/', views.IncidentCreateView.as_view(), name='incident_create'),
    path('incident/<int:pk>/', views.IncidentDetailView.as_view(), name='incident_detail'),
    path('incident/<int:pk>/update/', views.IncidentUpdateView.as_view(), name='incident_update'),
    path('incident/<int:pk>/delete/', views.IncidentDeleteView.as_view(), name='incident_delete'),
    path('incident/<int:pk>/status/', views.update_status, name='update_status'),
    path('notifications/', views.NotificationListView.as_view(), name='notifications'),
    path('notifications/read/', views.mark_notifications_read, name='mark_notifications_read'),
]
