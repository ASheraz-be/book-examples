from django.db import models
from oscar.apps.partner.abstract_models import AbstractStockRecord
# https://django-oscar.readthedocs.io/en/2.1.0/ref/apps/partner.html#oscar.apps.partner.abstract_models.AbstractStockRecord



class StockRecord(AbstractStockRecord):
    stock_nickname = models.CharField(max_length=100)

from oscar.apps.partner.models import *  # noqa isort:skip
