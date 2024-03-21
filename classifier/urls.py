from django.urls import path
from classifier.views import classifier

app_name = "classifier"

urlpatterns = [
    path("", classifier, name="index"),
]