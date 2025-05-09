from django.urls import path
from users.views import register,signIn,active,create_group,signOut

urlpatterns = [
    path('register/', register, name="register"),
    path('sign-in/', signIn, name="signIn"),
    path('sign-out/', signOut, name="signOut"),
    path('activate/<int:user_id>/<str:token>',active, name='active'),
    path('admin/create-group',create_group, name='create-group'),
]
