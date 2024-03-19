from django.urls import path
from accounts.views import  (
    clientRegistration, login_user,activate,log_out,edit_profile
)

app_name = "accounts"

urlpatterns = [
    path('login/', login_user, name='login'),
    path('register/', clientRegistration, name="sign-up"),
    path('update-profile/', edit_profile, name='update-profile'),
    path('logout/', log_out, name='logout'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    # path('reset/<str:uidb64>/<str:token>/<str:password>/', reset, name='reset'),
]