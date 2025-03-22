from django.shortcuts import render, get_object_or_404
from .models import News
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
    usd_to_try = data_dollar['rates'].get("TRY", "N/A")
    eur_to_try = data_eur['rates'].get("TRY", "N/A")

    return usd_to_try, eur_to_try

def home(request):

    news_items = News.objects.filter(category="politics")[:4]
    news_items_sports = News.objects.filter(category="sports")[:4]


    usd_to_try, eur_to_try = get_exchange_rates()


    return render(
        request,
        "taha/index.html",
        {
            "news_items": news_items,
            "news_items_sports": news_items_sports,
            "usd_to_try": usd_to_try,
            "eur_to_try": eur_to_try,
        },
    )


def news_details(request, id):
    # Burada, belirli bir haberin id'sine göre veriyi alıyoruz
    news_item = get_object_or_404(News, id=id)
    news_items_sports = News.objects.filter(category="sports")[:4]
    related_news = News.objects.filter(category=news_item.category).exclude(id=id)[:4]

    usd_to_try, eur_to_try = get_exchange_rates()

    return render(
        request,
        "taha/news_details.html",
        {
        "news_item": news_item, 
        "related_news": related_news,
        "usd_to_try": usd_to_try,
        "eur_to_try": eur_to_try,
        },
    )


def news_view(request):
    # Kategorilere göre haberleri grupla
    news_by_category = {}
    categories = News.objects.values_list(
        "category", flat=True
    ).distinct()  # Tüm kategoriler

    for category in categories:
        news_by_category[category] = News.objects.filter(
            category=category
        )  # Her kategoriye ait haberler

    return render(request, "taha/index.html", {"news_by_category": news_by_category})
