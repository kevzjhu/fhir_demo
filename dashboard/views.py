import json
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import *

fhir_base = "http://localhost:8080/fhir"


def index(request):

    if request.user.is_authenticated:

        if request.method == "GET" and "patient_id" in request.GET:
            print(request.GET)
            patient_id = request.GET["patient_id"]
            url = f"{fhir_base}/Patient/{patient_id}"
            response = requests.get(url)
            if response.status_code == 200:
                patient_data = response.json()
                return render(
                    request, "dashboard/index.html", {"patient": patient_data}
                )

        return render(request, "dashboard/index.html")
    else:
        return HttpResponseRedirect(reverse("login"))


# displays list of patients
def patient(request):
    pass


# need csrf token
@login_required
def create(request):

    if request.method == "POST":
        data = json.loads(request.body)
        print(data)

        response = requests.post(
            f"{fhir_base}/Patient",
            headers={"Content-Type": "application/fhir+json"},
            data=json.dumps(data),
        )
        return JsonResponse(response.json(), status=response.status_code)
        # return redirect("/dashboard/index.html")
    else:
        return render(request, "dashboard/create.html")


# login/logout/register
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "dashboard/login.html",
                {"message": "Invalid email and/or password."},
            )
    else:
        return render(request, "dashboard/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "dashboard/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(
                request,
                "dashboard/register.html",
                {"message": "Email address already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "dashboard/register.html")
