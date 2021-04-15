from oscar.apps.catalogue.abstract_models import AbstractProduct 
from django.db import models
# https://django-oscar.readthedocs.io/en/2.1.0/ref/apps/catalogue.html#oscar.apps.catalogue.abstract_models.AbstractProduct


class Product(AbstractProduct):
	nick_name = models.CharField(max_length=100)





from oscar.apps.catalogue.models import *  # noqa isort:skip
