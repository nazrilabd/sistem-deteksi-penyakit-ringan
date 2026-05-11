from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.projects, name='projects'),
      path('projects/<int:id>/', views.project_detail, name='project_detail'),
    path('certificates/', views.certificates, name='certificates'),
     path('certificates/<int:id>/', views.certificate_detail, name='certificate_detail'),
    path('skills/', views.skills, name='skills'),
    path('about/', views.about, name='about'),
]