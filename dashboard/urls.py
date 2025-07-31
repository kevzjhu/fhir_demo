from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("patient/<int:patient_id>", views.patient, name="patients"),
    path("create", views.create, name="create"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]
