from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *

@login_required
def portfolio(request):

    # TODO - get User from request, get FinanceUser, and fetch associate portfolio

    return render(request, "stocks/portfolio.html")

''' AJAX request handler for retrieving a stock quote '''
@login_required
@csrf_exempt
def quote(request):

    # Lookup via AJAX
    if request.method == 'POST':
        symbol = request.POST.get('symbol')

        try:
            stock = Stock(symbol)
        except StockLookupError:
            return JsonResponse({'error': 'TODO'})

        return JsonResponse({'symbol': stock.symbol, 'name': stock.name, 'price': stock.price})

    # GET request; render form
    else:
        return render(request, 'stocks/quote.html')

''' Handler for buying a stock (via AJAX) and display buy form '''
@login_required
@csrf_exempt
def buy(request):

    # Buy via AJAX
    if request.method == 'POST':
        number_of_shares = request.POST.get("shares")
        symbol = request.POST.get("symbol")
        # TODO - get FinanceUser

        try:
            StockHolding.buy_shares(symbol, number_of_shares)
        except StockLookupError:
            # TODO - add appropriate message
            return JsonResponse({'error': ''})

        # TODO - add appropriate message
        return JsonResponse({'success': ''})

    # Render form
    return render(request, 'stocks/buy.html')

''' Handler for selling a stock (via AJAX) and display sell form '''
@login_required
@csrf_exempt
def sell(request):

    # Sell via AJAX
    if request.method == 'POST':
        number_of_shares = request.POST.get("shares")
        symbol = request.POST.get("symbol")
        # TODO - get FinanceUser

        try:
            success = StockHolding.sell_shares(symbol, number_of_shares)
        except StockLookupError:
            # TODO - add appropriate message
            return JsonResponse({'error': 'TODO'})

        # TODO - add appropriate message
        return JsonResponse({'success': 'TODO'})

    # Return form
    return render(request, 'stocks/sell.html')