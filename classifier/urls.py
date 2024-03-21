from django.urls import path
from classifier.views import homepage, classifier_model

app_name = "classifier"

urlpatterns = [
    path('', homepage, name="home"),
    path("classifier_model/", classifier_model, name="classifier_model"),
]