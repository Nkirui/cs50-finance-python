from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *

@login_required
def portfolio(request):
    return render(request, "stocks/portfolio.html")

@csrf_exempt
def quote(request):

    # Lookup via AJAX
    if request.method == 'POST':
        symbol = request.POST.get('symbol')

        stock = Stock(symbol)

        return JsonResponse({'symbol': stock.symbol, 'name': stock.name, 'price': stock.price})

    # GET request; render form
    else:
        return render(request, 'stocks/quote.html')

def buy(request):
    # TODO
    return render(request, 'stocks/buy.html')

def sell(request):
    # TODO
    return render(request, 'stocks/sell.html')