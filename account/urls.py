from django.urls import path

from account.views import RegisterApiView, ActivationAPIView, LoginApiView

urlpatterns = [
    path('register/', RegisterApiView.as_view()),
    path('activate/<uuid:activation_code>/', ActivationAPIView.as_view()),
    path('login/', LoginApiView.as_view()),
]