
from django.urls import path
from guidance import views

urlpatterns = [
 path('', views.login_view, name='login'),
 path('signup/', views.signup_view, name='signup'),
 path('logout/', views.logout_view, name='logout'),
 path('dashboard/', views.dashboard, name='dashboard'),
 path('test/', views.career_test, name='career_test'),
 path('result/<int:result_id>/', views.career_result, name='career_result'),
 path('profile/', views.profile_view, name='profile'),
path('profile/update/', views.profile_update, name='profile_update'),
path('profile/change-password/', views.change_password, name='change_password'),
path('history/', views.career_history, name='career_history'),
path('history/delete/<int:result_id>/', views.delete_result, name='delete_result'),

]
