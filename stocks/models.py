from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Store additional information related to a user
class FinanceUser(models.Model):
    cash = models.IntegerField(default=10000)
    user = models.OneToOneField(User)

# Represents a stock
class Stock:

    def __init__(self, symbol):

        self.symbol = symbol

        # TODO - init with actual price/name info

        self.name = "Facebook, Inc."
        self.price = 15.50

# Represents a user's holding of a stock, including total shares and transactions for a given symbol
class StockHolding(models.Model):
    symbol = models.CharField(max_length=5)
    shares = models.IntegerField()
    owner = models.ForeignKey(User)

    def __init__(self, symbol, owner, shares=0):
        self.symbol = symbol
        self.shares = shares
        self.owner = owner

    def get_transactions(self):
        return self.transaction_set.all()

    @staticmethod
    def buy_shares(user, symbol, number_of_shares):
        stock = Stock(symbol)

        holding = StockHolding.objects.get_or_create(symbol=symbol, owner=user)
        holding.buy_shares(number_of_shares)
        Transaction.create(holding=holding, type="buy", price=stock.price)

    def buy_shares(self, number_of_shares):
        self.shares += number_of_shares

    @staticmethod
    def sell_shares(user, symbol, number_of_shares):
        stock = Stock(symbol)

        holding = StockHolding.objects.get_or_create(symbol=symbol, owner=user)
        holding.buy_shares(number_of_shares)
        Transaction.create(holding=holding, type="sell", price=stock.price)

    def sell_shares(self, number_of_shares):
        self.shares -= number_of_shares


# A given buy/sell transaction
class Transaction(models.Model):
    holding = models.ForeignKey(StockHolding)
    date = models.DateField(default=datetime.now)
    type = models.CharField(max_length=10) # "buy" or "sell"
    price = models.FloatField()
