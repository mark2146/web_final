from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('evaluate/', views.evaluation_form, name='evaluation_form'),
    path('evaluations/', views.evaluation_list, name='evaluation_list'),
    path('home/', views.home, name='home'), 
    path('course-bot/', views.course_bot, name='course_bot'),
    path('resume-generator/', views.resume_generator, name='resume_generator'),
    path('resume-download/', views.resume_download, name='resume_download'),  # 確保這一行正確
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
]
