from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about_us, name='about_us'),
    path('contact/', views.contact, name='contact'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='polls/login.html'), name='login'),
    path('accounts/signup/', views.signup, name='signup'),
    
    path('<int:poll_id>/', views.detail, name='detail'),
    path('polls/<int:poll_id>/age_chart/', views.age_chart, name='age_chart'),
    
    path('<int:poll_id>/results/', views.results, name='results'),
    path('<int:poll_id>/vote/', views.vote, name='vote'),
    path('<int:poll_id>/clear_vote/', views.clear_vote, name='clear_vote'),
]
