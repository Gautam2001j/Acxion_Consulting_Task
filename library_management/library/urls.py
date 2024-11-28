from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('admin-dash/',views.admin_dashboard, name='admin_dash'),
    path('maintenance/', views.maintenance_view, name='maintenance_view'),
    path('issue-book/', views.issue_book, name='issue_book'),
    path('logout/', views.logout_view, name='logout'),
]
