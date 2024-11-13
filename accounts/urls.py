from django.urls import path
from  . import views


urlpatterns=[
    path('register/',views.registerUser,name='register'),
    path('login/',views.loginUser,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('dashboard/',views.dashboard,name='admin-dashboard'),
    path('edit-user/<int:userId>/',views.edit_user,name='edit-user'),
    path('deleteUser/<int:userId>/',views.delete_user,name='delete-user'),
]