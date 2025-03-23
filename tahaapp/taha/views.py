from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import News, AboutContent, Category
import requests


# Create your views here.


def get_exchange_rates():
    urldollar = "https://api.exchangerate-api.com/v4/latest/USD"
    response_dollar = requests.get(urldollar)
    data_dollar = response_dollar.json()

    urleur = "https://api.exchangerate-api.com/v4/latest/EUR"
    response_eur = requests.get(urleur)
    data_eur = response_eur.json()

    usd_to_try = data_dollar["rates"].get("TRY", "N/A")
    eur_to_try = data_eur["rates"].get("TRY", "N/A")

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


# def about(request):
#     about_content = AboutContent.objects.all()
#     categories = Category.objects.all()
#     return render(request, "taha/about.html", 
#     {
#         'about_content': about_content,
#         'categories': categories
#     })
    
def about(request, category_id=None):
    if category_id:
        about_content = AboutContent.objects.filter(category_id=category_id)
    else:
        about_content = AboutContent.objects.all()
    
    categories = Category.objects.all()
    return render(request, 'about.html', {
        'about_content': about_content,
        'categories': categories,
        'category_id': category_id,
    })

def news_details(request, id):
    # if not request.user.is_authenticated: ##sadece login olanların görebiliceği kısım
    #     return redirect("login")

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
    news_by_category = {}
    categories = News.objects.values_list("category", flat=True).distinct()

    for category in categories:
        news_by_category[category] = News.objects.filter(category=category)

    return render(request, "taha/index.html", {"news_by_category": news_by_category})

