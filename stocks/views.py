from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *

# Display user portfolio
@login_required
def portfolio(request):

    # StockHolding objects are owned by a FinanceUser, so fetch the corresponding id first
    user = FinanceUser.objects.get(user_id=request.user.id)
    holdings = StockHolding.objects.filter(owner_id=user.id)
    user_portfolio = []
    total_value = 0

    # Build up data set for view display
    for holding in holdings:
        if holding.shares > 0:
            stock = Stock(holding.symbol)
            value = stock.price * holding.shares
            user_portfolio.append({
                'name': holding.symbol + ': ' + stock.name,
                'shares': holding.shares,
                'price': "$" + "{0:.2f}".format(stock.price),
                'value': "$" + "{0:.2f}".format(value)
            })
            total_value += value

    return render(request, "stocks/portfolio.html", {'portfolio': user_portfolio, 'total_value': "$" + "{0:.2f}".format(total_value)})

# AJAX request handler for retrieving a stock quote
@login_required
@csrf_exempt
def quote(request):

    # Lookup via AJAX
    if request.method == 'POST':
        symbol = request.POST.get('symbol')

        try:
            stock = Stock(symbol)
        except StockLookupError as err:
            return JsonResponse({'error': str(err)})

        return JsonResponse({'symbol': stock.symbol, 'name': stock.name, 'price': "{0:.2f}".format(stock.price)})

    # GET request; render form
    else:
        return render(request, 'stocks/quote.html')

# Handler for buying a stock (via AJAX) and display buy form
@login_required
@csrf_exempt
def buy(request):

    # Buy via AJAX
    if request.method == 'POST':
        number_of_shares = int(request.POST.get("shares"))
        symbol = request.POST.get("symbol")
        user = FinanceUser.objects.get(user_id=request.user.id)

        try:
            holding = StockHolding.buy_shares(user, symbol, number_of_shares)
        except (StockLookupError, StockTransactionError) as err:
            return JsonResponse({'error': str(err)})

        return JsonResponse({
            'success': str(number_of_shares) + ' shares of ' + symbol + ' purchased'
        })

    # Render form
    return render(request, 'stocks/buy.html')

# Handler for selling a stock (via AJAX) and display sell form
@login_required
@csrf_exempt
def sell(request):

    # Sell via AJAX
    if request.method == 'POST':
        number_of_shares = int(request.POST.get("shares"))
        symbol = request.POST.get("symbol")
        user = FinanceUser.objects.get(user_id=request.user.id)

        try:
            holding = StockHolding.sell_shares(user, symbol, number_of_shares)
        except (StockLookupError, StockTransactionError) as err:
            return JsonResponse({'error': str(err)})

        return JsonResponse({
            'success': str(number_of_shares) + ' shares of ' + symbol + ' sold'
        })

    # Return form
    return render(request, 'stocks/sell.html')