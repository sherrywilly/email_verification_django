from core.views import Activation, RegView, email
from django.urls import path

urlpatterns = [
    path("", RegView.as_view(), name="registration"),
    path('email/',email,name="email"),
    path('activate/<uidb64>/<token>/',Activation.as_view(),name="active")
]
