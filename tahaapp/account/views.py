from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import requests

# Create your views here.


def get_exchange_rates():
    # USD/TRY için API isteği
    urldollar = "https://api.exchangerate-api.com/v4/latest/USD"
    response_dollar = requests.get(urldollar)
    data_dollar = response_dollar.json()

    # EUR/TRY için API isteği
    urleur = "https://api.exchangerate-api.com/v4/latest/EUR"
    response_eur = requests.get(urleur)
    data_eur = response_eur.json()

    # Döviz kurları
    usd_to_try = data_dollar["rates"].get("TRY", "N/A")
    eur_to_try = data_eur["rates"].get("TRY", "N/A")

    return usd_to_try, eur_to_try


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(
                request, "account/login.html", {"error": "Email Veya Parola hatalı!"}
            )

    usd_to_try, eur_to_try = get_exchange_rates()

    return render(
        request,
        "account/login.html",
        {
            "usd_to_try": usd_to_try,
            "eur_to_try": eur_to_try,
        },
    )


def register_view(request):

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]

        if password == repassword:
            if User.objects.filter(username=username).exists():
                return render(
                    request,
                    "account/register.html",
                    {
                        "error": "username kullanılıyor!",
                        "username": username,
                        "email": email,
                        "firstname": firstname,
                        "lastname": lastname,
                    },
                )
            else:
                if User.objects.filter(email=email).exists():
                    return render(
                        request,
                        "account/register.html",
                        {
                            "error": "email kullanılıyor!",
                            "username": username,
                            "email": email,
                            "firstname": firstname,
                            "lastname": lastname,
                        },
                    )
                else:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        first_name=firstname,
                        last_name=lastname,
                        password=password,
                    )
                    user.save()
                    return redirect("login")
        else:
            return render(
                request,
                "account/register.html",
                {
                    "error": "parola eşleşmiyor",
                    "username": username,
                    "email": email,
                    "firstname": firstname,
                    "lastname": lastname,
                },
            )

    usd_to_try, eur_to_try = get_exchange_rates()

    return render(
        request,
        "account/register.html",
        {
            "usd_to_try": usd_to_try,
            "eur_to_try": eur_to_try,
        },
    )
