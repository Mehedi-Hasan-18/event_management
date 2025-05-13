from django.urls import path
from users.views import CreateGroupView,LogoutView,RegisterView,CustomLoginView,AccountActivationView,ProfileView,ChangePassword,PasswordChangeDoneView,CustomPasswordReseConfirmtView,CustomPasswordResetView,CustomLogoutView

urlpatterns = [
    # path('register/', register, name="register"),
    path('register/', RegisterView.as_view(), name="register"),
    path('sign-in/', CustomLoginView.as_view(), name="signIn"),
    path('sign-out/', CustomLogoutView.as_view(), name="signOut"),
    path('activate/<int:user_id>/<str:token>',AccountActivationView.as_view(), name='active'),
    path('admin/create-group',CreateGroupView.as_view(), name='create-group'),
    path('profile/',ProfileView.as_view(), name='profile' ),
    path('change-password/', ChangePassword.as_view(), name='change_password' ),
    path('change-password/done/', PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done/' ),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset' ),
    path('password-reset/confirm/<uidb64>/<token>', CustomPasswordReseConfirmtView.as_view(), name='password_reset_confirm' ),
]
