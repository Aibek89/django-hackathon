from django.urls import path

from account.views import RegisterApiView

urlpatterns = [
    path('register/', RegisterApiView.as_view()),
]