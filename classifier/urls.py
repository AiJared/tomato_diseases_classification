from django.urls import path
from classifier.views import classifier_model

app_name = "classifier"

urlpatterns = [
    path("classifier_model/", classifier_model, name="classifier_model"),
]